from django.db import models
from django.contrib.auth import get_user_model

from likes.models import Like


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        get_user_model(), db_column="user_id", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title

    def like(self, user):
        Like.objects.create(user=user, post=self)

    def get_likes(self):
        return Like.objects.filter(post=self)
