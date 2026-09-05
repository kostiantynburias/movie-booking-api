from rest_framework import serializers

from apps.reservations.models import Seat, Reservation, Ticket
from apps.showtimes.serializers import ShowtimeSerializer


class SeatSerializer(serializers.ModelSerializer):
    """Base serializer for physical seat representation."""

    class Meta:
        model = Seat
        fields = ['id', 'row_number', 'seat_number']


class SeatAvailabilitySerializer(serializers.ModelSerializer):
    """Serializer for interactive hall seat layout with booking status."""

    is_available = serializers.BooleanField(read_only=True)

    class Meta:
        model = Seat
        fields = ['id', 'row_number', 'seat_number', 'is_available']


class TicketSerializer(serializers.ModelSerializer):
    """Serializer for individual tickets with nested seat details."""

    seat = SeatSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'seat']


class ReservationCreateSerializer(serializers.ModelSerializer):
    """Serializer for validating booking requests."""

    seat_ids = serializers.ListField(
        child=serializers.IntegerField(), 
        write_only=True, 
        allow_empty=False
    )

    class Meta:
        model = Reservation
        fields = ['id', 'showtime', 'seat_ids']

    def validate_seat_ids(self, value):
        if len(value) != len(set(value)):
            raise serializers.ValidationError("Список місць не може містити дублікати.")
        return value


class ReservationDetailSerializer(serializers.ModelSerializer):
    """Serializer for full reservation view with embedded tickets."""

    tickets = TicketSerializer(many=True, read_only=True)
    showtime = ShowtimeSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = ['id', 'user', 'showtime', 'status', 'created_at', 'tickets']


class AdminReservationDetailSerializer(ReservationDetailSerializer):
    """Extended detail serializer for admins."""
    ...
    

class ReservationListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for user's reservation history."""

    tickets_count = serializers.SerializerMethodField()
    showtime = ShowtimeSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = ['id', 'showtime', 'status', 'created_at', 'tickets_count']

    def get_tickets_count(self, obj):
        return len(obj.tickets.all())