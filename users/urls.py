from django.urls import path, include

from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import UserPasswordViewSet, UserViewSet


router = DefaultRouter()
router.register("", UserViewSet, basename="users")
router.register("password", UserPasswordViewSet, basename="password")

urlpatterns = [
    path('auth/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path("users/", include(router.urls))
]
