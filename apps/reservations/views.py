from django.db import transaction
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.reservations.models import Reservation, Ticket, Seat
from apps.reservations.serializers import (
    ReservationCreateSerializer,
    ReservationDetailSerializer,
    ReservationListSerializer,
)


class ReservationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling reservation operations.
    Supports creating bookings atomically, listing user's history, and canceling bookings.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Reservation.objects.prefetch_related('tickets__seat')

        if user.is_staff:
            return queryset
        return queryset.filter(user=user)

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

        try:
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

                existing_tickets = Ticket.objects.filter(
                    showtime=showtime,
                    seat__in=seats
                ).exists()

                if existing_tickets:
                    return Response(
                        {"detail": "Одне або декілька обраних місць уже заброньовані."},
                        status=status.HTTP_409_CONFLICT
                    )

                reservation = Reservation.objects.create(
                    user=self.request.user,
                    showtime=showtime,
                    status=Reservation.Status.PENDING
                )

                tickets_to_create = [
                    Ticket(reservation=reservation, showtime=showtime, seat=seat)
                    for seat in seats
                ]
                Ticket.objects.bulk_create(tickets_to_create)

        except Exception as e:
            return Response(
                {"detail": f"Помилка при обробці транзакції: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        response_serializer = ReservationDetailSerializer(reservation)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel(self, request, pk=None):
        """Allows a user to cancel their pending/confirmed reservation."""
        reservation = self.get_object()

        if reservation.status == Reservation.Status.CANCELLED:
            return Response(
                {"detail": "Це бронювання вже скасовано."},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            reservation.status = Reservation.Status.CANCELLED
            reservation.save()

            reservation.tickets.all().delete()

        return Response(
            {"detail": "Бронювання успішно скасовано."},
            status=status.HTTP_200_OK
        )