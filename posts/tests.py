from django.test import TestCase
from django.contrib.auth import get_user_model

from posts.models import Post


class PostTests(TestCase):
    def test_create_post(self):
        user_model = get_user_model()
        user = user_model.objects.create_superuser(
            "email@example.com", "user_name", "password"
        )
        post = Post.objects.create(
            title="Test title", content="Test content", author=user
        )
        self.assertEqual(post.title, "Test title")
        self.assertEqual(post.content, "Test content")

    def test_create_retrieve(self):
        user_model = get_user_model()
        user = user_model.objects.create_superuser(
            "email@example.com", "user_name", "password"
        )
        post = Post.objects.create(
            title="Test title", content="Test content", author=user
        )
        self.assertEqual(post.title, "Test title")
        self.assertEqual(post.content, "Test content")
        post = Post.objects.get(id=post.id)
        self.assertEqual(post.title, "Test title")
        self.assertEqual(post.content, "Test content")

    def test_create_update_post(self):
        user_model = get_user_model()
        user = user_model.objects.create_superuser(
            "email@example.com", "user_name", "password"
        )
        post = Post.objects.create(
            title="Test title", content="Test content", author=user
        )
        self.assertEqual(post.title, "Test title")
        self.assertEqual(post.content, "Test content")
        post.title = "New title"
        post.content = "New content"
        self.assertEqual(post.title, "New title")
        self.assertEqual(post.content, "New content")

    def test_create_delete_post(self):
        user_model = get_user_model()
        user = user_model.objects.create_superuser(
            "email@example.com", "user_name", "password"
        )
        post = Post.objects.create(
            title="Test title", content="Test content", author=user
        )
        self.assertEqual(post.title, "Test title")
        self.assertEqual(post.content, "Test content")
        post.delete()
        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(id=post.id)
