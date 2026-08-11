from decimal import Decimal
from rest_framework import serializers

from apps.showtimes.models import Showtime
from apps.movies.serializers import MovieDetailSerializer


class ShowtimeSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving showtime details.

    Provides read-only information about a movie showtime, including nested
    movie details and the automatically calculated end time with cleaning.
    """

    movie = MovieDetailSerializer(read_only=True)
    end_time_with_cleaning = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Showtime
        fields = ["id", "movie", "start_time", "end_time_with_cleaning", "price"]


class ShowtimeCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating movie showtimes.

    Handles write operations for showtimes and triggers model-level validation
    to ensure that showtimes do not overlap in the hall (accounting for a 20-minute
    cleaning break after each movie).
    """

    class Meta:
        model = Showtime
        fields = ["id", "movie", "start_time", "price"]

    def validate(self, attrs):
        movie = attrs.get("movie", getattr(self.instance, "movie", None))
        start_time = attrs.get("start_time", getattr(self.instance, "start_time", None))
        price = attrs.get("price", getattr(self.instance, "price", Decimal("0.00")))

        instance = Showtime(
            movie=movie,
            start_time=start_time,
            price=price,
        )

        if self.instance:
            instance.pk = self.instance.pk

        try:
            instance.clean()
        except Exception as e:
            if hasattr(e, "message_dict"):
                raise serializers.ValidationError(e.message_dict)
            raise serializers.ValidationError(str(e))

        return attrs