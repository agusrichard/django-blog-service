from django.test import TestCase
from django.contrib.auth import get_user_model

from posts.models import Post


class PostTests(TestCase):
    def create_user_post(self):
        user_model = get_user_model()
        user = user_model.objects.create_superuser(
            "email@example.com", "user_name", "password"
        )
        post = Post.objects.create(
            title="Test title", content="Test content", author=user
        )

        return user, post

    def test_create_post(self):
        _, post = self.create_user_post()
        self.assertEqual(post.title, "Test title")
        self.assertEqual(post.content, "Test content")

    def test_create_retrieve(self):
        _, post = self.create_user_post()
        self.assertEqual(post.title, "Test title")
        self.assertEqual(post.content, "Test content")
        post = Post.objects.get(id=post.id)
        self.assertEqual(post.title, "Test title")
        self.assertEqual(post.content, "Test content")

    def test_create_update_post(self):
        _, post = self.create_user_post()
        self.assertEqual(post.title, "Test title")
        self.assertEqual(post.content, "Test content")
        post.title = "New title"
        post.content = "New content"
        self.assertEqual(post.title, "New title")
        self.assertEqual(post.content, "New content")

    def test_create_delete_post(self):
        _, post = self.create_user_post()
        self.assertEqual(post.title, "Test title")
        self.assertEqual(post.content, "Test content")
        post.delete()
        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(id=post.id)

    def test_create_comment(self):
        user, post = self.create_user_post()
        post.add_comment(user, "Test comment")
        self.assertEqual(post.get_comments().count(), 1)
