from django.urls import path

from posts.views import (
    PostCommentView,
    PostListCreateView,
    PostRetrieveUpdateDestroyView,
)

app_name = "posts"

urlpatterns = [
    path(
        "<int:pk>/",
        PostRetrieveUpdateDestroyView.as_view(),
        name="retrieve_update_destroy_posts",
    ),
    path("", PostListCreateView.as_view(), name="list_create_posts"),
    path("comments/<int:post_id>/", PostCommentView.as_view(), name="comment_posts"),
]
