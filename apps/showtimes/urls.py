from rest_framework.routers import DefaultRouter
from .views import ShowtimeViewSet

app_name = 'showtimes'

router = DefaultRouter()
router.register(r"showtimes", ShowtimeViewSet, basename="showtime")

urlpatterns = router.urls