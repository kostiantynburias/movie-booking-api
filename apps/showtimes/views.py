from django.db.models import Exists, OuterRef
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.showtimes.models import Showtime
from apps.showtimes.serializers import ShowtimeSerializer, ShowtimeCreateUpdateSerializer
from apps.showtimes.filters import ShowtimeFilter
from apps.reservations.models import Seat, Ticket
from apps.reservations.serializers import SeatAvailabilitySerializer
from core.permissions import IsAdminOrReadOnly


class ShowtimeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing movie showtimes.

    Supports listing, retrieving, creating, updating, and deleting showtimes.
    Filtering by movie ID and specific date (`?date=YYYY-MM-DD`) is supported.
    """

    queryset = Showtime.objects.select_related('movie')
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = ShowtimeFilter

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ShowtimeCreateUpdateSerializer
        return ShowtimeSerializer

    @action(
            detail=True, 
            methods=['get'], 
            url_path='seats',
            serializer_class=SeatAvailabilitySerializer
    )
    def seats(self, request, pk=None):
        """Retrieve the seating layout with availability status for a specific showtime."""
        showtime = self.get_object()

        ticket_exists = Ticket.objects.filter(
            showtime=showtime,
            seat=OuterRef('pk')
        )
        seats = Seat.objects.annotate(
            is_available=~Exists(ticket_exists)
        )

        serializer = SeatAvailabilitySerializer(seats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)