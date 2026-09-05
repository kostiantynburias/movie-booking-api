from django.db import transaction
from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import mixins, viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.reservations.models import Reservation, Ticket, Seat
from apps.reservations.serializers import (
    ReservationCreateSerializer,
    ReservationDetailSerializer,
    ReservationListSerializer,
    AdminReservationDetailSerializer
)
from apps.reservations.tasks import send_ticket_email_task


@extend_schema_view(
    list=extend_schema(
        tags=['customer profile'],
        summary='Get customer reservations list'
    ),
    retrieve=extend_schema(
        tags=['customer profile'],
        summary='Get specific customer reservation'
    ),
    create=extend_schema(
        tags=['customer profile'],
        summary='Create new reservation'
    ),
)
class UserReservationsViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """
    ViewSet for managing user-specific reservations.

    Allows authenticated users to view, create, cancel, and confirm
    their reservations.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            Reservation.objects
            .select_related('showtime', 'user')
            .prefetch_related('tickets__seat')
            .filter(user=self.request.user)
        )

    def get_serializer_class(self):
        if self.action == 'create':
            return ReservationCreateSerializer
        elif self.action == 'list':
            return ReservationListSerializer
        return ReservationDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        showtime = serializer.validated_data['showtime']
        seat_ids = serializer.validated_data['seat_ids']

        with transaction.atomic():
            seats = list(
                Seat.objects.filter(id__in=seat_ids)
                .order_by('id')
                .select_for_update()
            )

            if len(seats) != len(seat_ids):
                return Response(
                    {"detail": "Одне або декілька вказаних місць не існують."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            occupied_tickets = Ticket.objects.filter(
                showtime=showtime,
                seat__in=seats,
                reservation__status__in=[
                    Reservation.StatusChoices.PENDING,
                    Reservation.StatusChoices.CONFIRMED,
                ]
            ).exists()

            if occupied_tickets:
                return Response(
                    {"detail": "Одне або декілька обраних місць уже заброньовані."},
                    status=status.HTTP_409_CONFLICT
                )

            reservation = Reservation.objects.create(
                user=self.request.user,
                showtime=showtime,
                status=Reservation.StatusChoices.PENDING
            )

            tickets_to_create = [
                Ticket(reservation=reservation, showtime=showtime, seat=seat)
                for seat in seats
            ]
            Ticket.objects.bulk_create(tickets_to_create)

        response_serializer = ReservationDetailSerializer(reservation)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary='Cancel reservation',
        tags=['customer profile'],
        responses={
            200: OpenApiResponse(description="Бронювання успішно скасовано."),
            400: OpenApiResponse(description="Бронювання вже скасовано."),
        }
    )
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Allows a user to cancel their pending/confirmed reservation."""
        reservation = self.get_object()

        if reservation.status == Reservation.StatusChoices.CANCELLED:
            return Response(
                {"detail": "Це бронювання вже скасовано."},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            reservation.status = Reservation.StatusChoices.CANCELLED
            reservation.save(update_fields=['status'])

            reservation.tickets.all().delete()

        return Response(
            {"detail": "Бронювання успішно скасовано."},
            status=status.HTTP_200_OK
        )

    @extend_schema(
        summary='Confirm reservation',
        tags=['customer profile'],
        responses={
            200: ReservationDetailSerializer,
            400: OpenApiResponse(description="Неможливо підтвердити бронювання."),
        }
    )
    @action(detail=True, methods=['post'], url_path='confirm')
    def confirm(self, request, pk=None):
        """Allows a user to confirm their pending reservation."""
        reservation = self.get_object()

        if reservation.status != Reservation.StatusChoices.PENDING:
            return Response(
                {"detail": f"Неможливо підтвердити бронювання зі статусом {reservation.status}."},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            reservation.status = Reservation.StatusChoices.CONFIRMED
            reservation.save(update_fields=['status'])
            transaction.on_commit(lambda: send_ticket_email_task.delay(reservation.id))

        return Response(ReservationDetailSerializer(reservation).data, status=status.HTTP_200_OK)
        

@extend_schema_view(
    list=extend_schema(
        tags=['admin: reservations'],
        summary='Get all system reservations'
    ),
    retrieve=extend_schema(
        tags=['admin: reservations'],
        summary='Get detailed reservation'
    ),
    update=extend_schema(
        tags=['admin: reservations'],
        summary='Full reservation update'
    ),
    partial_update=extend_schema(
        tags=['admin: reservations'],
        summary='Partial reservation update'
    ),
    destroy=extend_schema(
        tags=['admin: reservations'],
        summary='Delete reservation'
    ),
)
class AdminReservationsViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """
    ViewSet for administrative management of all reservations.

    Allows administrators to view, update, and delete any reservation in the system.
    Creation is disabled to prevent bypassing business logic.
    """

    permission_classes = [permissions.IsAdminUser]
    queryset = Reservation.objects.select_related('showtime', 'user').prefetch_related('tickets__seat').all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ReservationListSerializer
        return AdminReservationDetailSerializer
