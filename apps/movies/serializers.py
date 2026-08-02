from rest_framework import serializers

from apps.movies.models import Genre, Movie


class GenreSerializer(serializers.ModelSerializer):
    """
    Serializer for the Genre model.

    Handles serialization and validation for movie genres.
    The 'slug' and 'id' fields are read-only as they are auto-generated.
    """

    class Meta:
        model = Genre
        fields = ['id', 'name', 'slug']
        read_only_fields = ['id', 'slug']


class MovieSerializer(serializers.ModelSerializer):
    """
    Serializer for listing movies (lightweight representation).
    """

    genres = serializers.SlugRelatedField(
        many=True, 
        read_only=True, 
        slug_field='name',
    )

    class Meta:
        model = Movie
        fields = ['id', 'title', 'duration', 'genres', 'poster', 'release_date']
        read_only_fields = ['id']


class MovieDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed view of a movie.
    """

    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'description', 
            'duration', 'genres', 'poster', 
            'release_date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class MovieCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating movies (admin use).
    """

    genres = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Genre.objects.all()
    )

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'description', 
            'duration', 'genres', 'poster', 'release_date'
        ]
        read_only_fields = ['id']