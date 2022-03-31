from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import (
    UserCreateView,
    UserActivateView,
    UserRetrieveUpdateView,
    CustomTokenObtainPairView,
)

app_name = "users"

urlpatterns = [
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", UserRetrieveUpdateView.as_view(), name="retrieve_user"),
    path("activate/", UserActivateView.as_view(), name="activate_user"),
    path("", UserCreateView.as_view(), name="create_user"),
]
