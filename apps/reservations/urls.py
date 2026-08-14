from rest_framework.routers import DefaultRouter

from apps.reservations.views import ReservationViewSet

app_name = 'reservations'

router = DefaultRouter()
router.register(r'reservations', ReservationViewSet, basename="reservations")

urlpatterns = router.urls