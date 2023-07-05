from rest_framework.routers import DefaultRouter

from phone_cases.views import PhoneCaseViewSet


router = DefaultRouter()
router.register("phone-cases", PhoneCaseViewSet, basename="phone-cases")

urlpatterns = router.urls
