from django_filters import rest_framework as filters

from apps.movies.models import Movie


class MovieFilter(filters.FilterSet):
    """
    FilterSet for the Movie model.

    Allows filtering movies by genre (slug or ID), duration range,
    and partial title search.
    """
    
    genre = filters.CharFilter(field_name='genres__slug', lookup_expr='iexact')
    genre_id = filters.NumberFilter(field_name='genres__id')
    duration_min = filters.NumberFilter(field_name='duration', lookup_expr='gte')
    duration_max = filters.NumberFilter(field_name='duration', lookup_expr='lte')
    search = filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = Movie
        fields = ['genre', 'genre_id', 'duration_min', 'duration_max', 'search']