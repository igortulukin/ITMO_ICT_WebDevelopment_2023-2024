from rest_framework.routers import SimpleRouter
from . import views


router = SimpleRouter()

router.register('workers', views.WorkerViewSet)
router.register('workers/schedule', views.CleaningViewSet)

router.register('visiters', views.VisiterViewSet)
router.register("visiters/from", views.CityViewSet)
router.register('visiters/living', views.LivingViewSet)

router.register('floor', views.FloorViewSet)
router.register('floor/rooms', views.RoomViewSet)

urlpatterns = router.urls
