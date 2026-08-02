from rest_framework import viewsets

from apps.movies.models import Genre, Movie
from apps.movies.serializers import (
    GenreSerializer,
    MovieSerializer,
    MovieDetailSerializer,
    MovieCreateUpdateSerializer
)
from apps.movies.permissions import IsAdminOrReadOnly


class GenreViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing genres.
    Allows public read-only access (GET), but restricts create/update/delete to admins.
    """
    
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    permission_classes = (IsAdminOrReadOnly,)


class MovieViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing movies.
    Provides list, detail, create, update, and delete actions.
    """

    queryset = Movie.objects.prefetch_related('genres')
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieSerializer
        elif self.action == 'retrieve':
            return MovieDetailSerializer
        return MovieCreateUpdateSerializer