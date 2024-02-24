from rest_framework.routers import SimpleRouter
from . import views


router = SimpleRouter()

router.register('workers', views.WorkerViewSet)
router.register('schedule', views.CleaningViewSet)

router.register('visiters', views.VisiterViewSet)
router.register("from", views.CityViewSet)
router.register('living', views.LivingViewSet)

router.register('floor', views.FloorViewSet)
router.register('rooms', views.RoomViewSet)

urlpatterns = router.urls
