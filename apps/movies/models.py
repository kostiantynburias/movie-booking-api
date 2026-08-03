from django.db import models
from slugify import slugify


class Genre(models.Model):
    """
    Represents a movie genre (e.g., Action, Sci-Fi, Drama).

    Stores genre names and automatically generates unique URL-friendly slugs 
    upon saving if not explicitly provided.
    """

    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанри'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Movie(models.Model):
    """
    Represents a movie in the cinema catalog.

    Contains core metadata such as title, description, duration in minutes,
    associated genres, poster image, and release details.
    """

    title = models.CharField(max_length=150, db_index=True)
    description = models.TextField()
    duration = models.PositiveIntegerField(
        default=60, 
        help_text='Час в хвилинах.', 
        db_index=True
    )
    genres = models.ManyToManyField(Genre, related_name='movies')
    poster = models.ImageField(upload_to='posters/')
    release_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Фільм'
        verbose_name_plural = 'Фільми'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} - {self.duration} хв.'