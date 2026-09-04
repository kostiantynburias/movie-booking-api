from django.urls import path, include
from rest_framework.routers import SimpleRouter
from apps.reservations.views import UserReservationsViewSet, AdminReservationsViewSet

router = SimpleRouter()

router.register(r'users/me/reservations', UserReservationsViewSet, basename='user-reservations')

router.register(r'admin/reservations', AdminReservationsViewSet, basename='admin-reservations')

urlpatterns = [
    path('', include(router.urls)),
]