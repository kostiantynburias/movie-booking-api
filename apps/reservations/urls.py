from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.reservations.views import UserReservationsViewSet, AdminReservationsViewSet

router = DefaultRouter()

router.register(r'users/me/reservations', UserReservationsViewSet, basename='user-reservations')
router.register(r'admin/reservations', AdminReservationsViewSet, basename='admin-reservations')

urlpatterns = router.urls