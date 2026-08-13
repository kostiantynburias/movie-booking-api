import django_filters

from apps.showtimes.models import Showtime


class ShowtimeFilter(django_filters.FilterSet):
    """
    FilterSet for Showtime model to allow filtering by movie ID and specific date.
    """

    date = django_filters.DateFilter(
        field_name='start_time',
        lookup_expr='date',
        help_text="Filter showtimes by specific date (YYYY-MM-DD)"
    )

    class Meta:
        model = Showtime
        fields = ["movie", "date"]