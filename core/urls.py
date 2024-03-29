from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include("users.urls", namespace="users")),
    path("api/posts/", include("posts.urls", namespace="posts")),
    path("api/likes/", include("likes.urls", namespace="likes")),
]
