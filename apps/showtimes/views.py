from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from apps.showtimes.models import Showtime
from apps.showtimes.serializers import ShowtimeSerializer, ShowtimeCreateUpdateSerializer
from apps.movies.permissions import IsAdminOrReadOnly
from apps.showtimes.filters import ShowtimeFilter


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