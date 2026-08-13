from django.db import models
from django.contrib.auth import get_user_model

from apps.showtimes.models import Showtime

User = get_user_model()


class Seat(models.Model):
    """
    Represents a physical seat in the cinema hall.

    Stores row and seat positions. Ensures unique seating grid layout 
    to prevent duplicate seat definitions within the single cinema hall.
    """

    row_number = models.PositiveIntegerField()
    seat_number = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Місце'
        verbose_name_plural = 'Місця'
        ordering = ['row_number', 'seat_number']
        constraints = [
            models.UniqueConstraint(
                fields=['row_number', 'seat_number'], 
                name='unique_row_seat'
            )
        ]

    def __str__(self):
        return f'{self.row_number} ряд, {self.seat_number} місце'


class Reservation(models.Model):
    """
    Represents a user's booking order for a specific showtime.

    Tracks reservation status (pending, confirmed, cancelled) and creation timestamp.
    Used for temporal holding of seats before payment or ticket confirmation.
    """

    class StatusChoices(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        CANCELLED = 'cancelled', 'Cancelled'

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='reservations'
    )
    showtime = models.ForeignKey(
        Showtime, 
        on_delete=models.CASCADE, 
        related_name='reservations'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=15, 
        choices=StatusChoices.choices, 
        default=StatusChoices.PENDING
    )

    class Meta:
        verbose_name = 'Бронювання'
        verbose_name_plural = 'Бронювання'
        ordering = ['-created_at']

    def __str__(self):
        return f'Бронювання #{self.pk} ({self.showtime}) — {self.user}'


class Ticket(models.Model):
    """
    Represents an individual issued ticket linking a seat to a showtime and reservation.

    Enforces unique constraint on showtime and seat to hardware-block double-booking 
    and overbooking at the database layer.
    """

    reservation = models.ForeignKey(
        Reservation, 
        on_delete=models.CASCADE, 
        related_name='tickets'
    )
    showtime = models.ForeignKey(
        Showtime, 
        on_delete=models.CASCADE, 
        related_name='tickets'
    )
    seat = models.ForeignKey(
        Seat, 
        on_delete=models.CASCADE, 
        related_name='tickets'
    )

    class Meta:
        verbose_name = 'Квиток'
        verbose_name_plural = 'Квитки'
        constraints = [
            models.UniqueConstraint(
                fields=['showtime', 'seat'], 
                name='unique_showtime_seat'
            )
        ]

    def __str__(self):
        return f'Квиток #{self.pk} — {self.showtime} ({self.seat})'
