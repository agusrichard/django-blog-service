from django.urls import path

from likes.views import like_post, get_likes

app_name = "likes"

urlpatterns = [
    path("like_post/<int:post_id>/", like_post, name="like_post"),
    path("get_likes/<int:post_id>/", get_likes, name="get_likes"),
]
