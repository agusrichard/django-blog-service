from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from posts.models import Post

CONST_TITLE = "Test title"
CONST_CONTENT = "Test content"
CONST_EMAIL = "email@example.com"
CONST_USERNAME = "user_name"
CONST_PASSWORD = "password"
CONST_LIST_CREATE_POST = reverse("posts:list_create_posts")


class PostTests(TestCase):
    def create_user_post(self):
        user_model = get_user_model()
        user = user_model.objects.create_superuser(
            "email@example.com", "user_name", "password"
        )
        post = Post.objects.create(
            title=CONST_TITLE, content=CONST_CONTENT, author=user
        )

        return user, post

    def test_create_post(self):
        _, post = self.create_user_post()
        self.assertEqual(post.title, CONST_TITLE)
        self.assertEqual(post.content, CONST_CONTENT)

    def test_create_retrieve(self):
        _, post = self.create_user_post()
        self.assertEqual(post.title, CONST_TITLE)
        self.assertEqual(post.content, CONST_CONTENT)
        post = Post.objects.get(id=post.id)
        self.assertEqual(post.title, CONST_TITLE)
        self.assertEqual(post.content, CONST_CONTENT)

    def test_create_update_post(self):
        _, post = self.create_user_post()
        self.assertEqual(post.title, CONST_TITLE)
        self.assertEqual(post.content, CONST_CONTENT)
        post.title = "New title"
        post.content = "New content"
        self.assertEqual(post.title, "New title")
        self.assertEqual(post.content, "New content")

    def test_create_delete_post(self):
        _, post = self.create_user_post()
        self.assertEqual(post.title, CONST_TITLE)
        self.assertEqual(post.content, CONST_CONTENT)
        post.delete()
        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(id=post.id)

    def test_create_comment(self):
        user, post = self.create_user_post()
        post.add_comment(user, "Test comment")
        self.assertEqual(post.get_comments().count(), 1)


class PostAPITests(APITestCase):
    def setUp(self):
        url = reverse("users:create_user")
        data = {
            "email": CONST_EMAIL,
            "user_name": CONST_USERNAME,
            "password": CONST_PASSWORD,
        }

        self.client.post(url, data, format="json")

        url = reverse("users:activate_user")
        self.client.post(url, data, format="json")

        url = reverse("users:token_obtain_pair")
        response = self.client.post(url, data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + response.data["access"])

    def test_create_post(self):
        url = reverse("posts:list_create_posts")
        data = {"title": "Title", "content": "Content"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_single_post(self):
        self.create_post()
        response = self.client.get(CONST_LIST_CREATE_POST)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_multiple_post(self):
        num_posts = 10
        for _ in range(num_posts):
            self.create_post()

        response = self.client.get(CONST_LIST_CREATE_POST)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), num_posts)

    def create_post(self):
        data = {"title": "Title", "content": "Content"}
        self.client.post(CONST_LIST_CREATE_POST, data, format="json")
