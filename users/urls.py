from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import (
    UserCreateView,
    UserRetrieveView,
    CustomTokenObtainPairView,
)

app_name = "users"

urlpatterns = [
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("profile/", UserRetrieveView.as_view(), name="retrieve_user"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", UserCreateView.as_view(), name="create_user"),
]
