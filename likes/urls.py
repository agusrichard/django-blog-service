from django.urls import path

from likes.views import like_post, get_likes, unlike_post

app_name = "likes"

urlpatterns = [
    path("like_post/<int:post_id>/", like_post, name="like_post"),
    path("unlike_post/<int:post_id>/", unlike_post, name="unlike_post"),
    path("get_likes/<int:post_id>/", get_likes, name="get_likes"),
]
