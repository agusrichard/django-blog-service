from django.test import TestCase

from posts.models import Post


class PostTests(TestCase):
    def test_create_post(self):
        post = Post.objects.create(
            title="Test title",
            content="Test content",
        )
        self.assertEqual(post.title, "Test title")
        self.assertEqual(post.content, "Test content")

    def test_create_retrieve(self):
        post = Post.objects.create(
            title="Test title",
            content="Test content",
        )
        self.assertEqual(post.title, "Test title")
        self.assertEqual(post.content, "Test content")
        post = Post.objects.get(id=post.id)
        self.assertEqual(post.title, "Test title")
        self.assertEqual(post.content, "Test content")

    def test_create_update_post(self):
        post = Post.objects.create(
            title="Test title",
            content="Test content",
        )
        self.assertEqual(post.title, "Test title")
        self.assertEqual(post.content, "Test content")
        post.title = "New title"
        post.content = "New content"
        self.assertEqual(post.title, "New title")
        self.assertEqual(post.content, "New content")

    def test_create_delete_post(self):
        post = Post.objects.create(
            title="Test title",
            content="Test content",
        )
        self.assertEqual(post.title, "Test title")
        self.assertEqual(post.content, "Test content")
        post.delete()
        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(id=post.id)
