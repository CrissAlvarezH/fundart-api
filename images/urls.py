from rest_framework.routers import DefaultRouter

from images.views import ImageViewSet

router = DefaultRouter()

router.register(r"images", ImageViewSet, basename="images")

urlpatterns = router.urls
