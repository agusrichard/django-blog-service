from django.db import models


class Like(models.Model):
    user = models.ForeignKey(
        "users.User", related_name="user_likes", on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        "posts.Post", related_name="post_likes", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("user", "post"),)
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.user} likes {self.post}"
