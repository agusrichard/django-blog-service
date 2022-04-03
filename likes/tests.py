from django.test import TestCase

from users.models import User
from posts.models import Post


class LikeTests(TestCase):
    def test_create_like(self):
        new_user = User.objects.create_user(
            "email@example.com", "user_name", "password"
        )
        post = Post.objects.create(
            title="Test title", content="Test content", author=new_user
        )
        post.like(new_user)
        self.assertEqual(post.likes.count(), 1)
        return new_user, post

    def test_create_delete_like(self):
        user, post = self.test_create_like()
        post.unlike(user)
        self.assertEqual(post.likes.count(), 0)
