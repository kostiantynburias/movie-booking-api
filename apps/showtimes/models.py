from datetime import timedelta
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models

from apps.movies.models import Movie


class Showtime(models.Model):
    """
    Represents a movie showtime in the cinema schedule.

    Tracks start times and ticket prices. Validates hall availability to prevent 
    schedule overlaps, automatically incorporating a 20-minute cleaning break 
    after each screening.
    """

    movie = models.ForeignKey(
        Movie, 
        on_delete=models.CASCADE,
        related_name='showtimes'
    )
    start_time = models.DateTimeField(db_index=True)
    price = models.DecimalField(
        default=Decimal("0.00"), 
        max_digits=8, 
        decimal_places=2
    )

    class Meta:
        verbose_name = 'Сеанс'
        verbose_name_plural = 'Сеанси'
        ordering = ['-start_time']

    @property
    def end_time_with_cleaning(self):
        """Calculates the showtime end time including the 20-minute technical cleaning break."""
        if self.movie and self.start_time:
            return self.start_time + timedelta(minutes=self.movie.duration + 20)
        return None

    def clean(self):
        """Validates that the showtime does not overlap with existing showtimes."""
        super().clean()

        if not self.movie or not self.start_time:
            return

        new_end_time = self.end_time_with_cleaning

        overlapping_showtimes = Showtime.objects.select_related("movie").filter(
            start_time__lt=new_end_time
        )

        if self.pk:
            overlapping_showtimes = overlapping_showtimes.exclude(pk=self.pk)

        for existing in overlapping_showtimes:
            if new_end_time > existing.start_time and self.start_time < existing.end_time_with_cleaning:
                raise ValidationError(
                    {
                        "start_time": (
                            f"Сеанс перетинається з існуючим сеансом '{existing.movie.title}' "
                            f"({existing.start_time.strftime('%H:%M')} - "
                            f"{existing.end_time_with_cleaning.strftime('%H:%M')} з урахуванням прибирання)."
                        )
                    }
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.movie.title} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"