from django.db import models
from django.contrib.auth import get_user_model

from likes.models import Like
from comments.models import Comment


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        get_user_model(), db_column="user_id", on_delete=models.CASCADE
    )
    likes = models.ManyToManyField(
        get_user_model(), through=Like, related_name="liked_posts"
    )

    def __str__(self):
        return self.title

    def like(self, user):
        Like.objects.create(user=user, post=self)

    def unlike(self, user):
        Like.objects.filter(user=user, post=self).delete()

    def get_likes(self):
        return self.likes.all()

    def add_comment(self, user, content):
        comment = Comment(user=user, post=self, content=content)
        comment.save()

    def get_comments(self):
        return Comment.objects.filter(post=self)
