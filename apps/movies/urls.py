from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.movies.views import GenreViewSet, MovieViewSet

app_name = 'movies'

router = DefaultRouter()
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'movies', MovieViewSet, basename='movie')

urlpatterns = router.urls