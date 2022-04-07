from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from posts.models import Post

CONST_TITLE = "Test title"
CONST_CONTENT = "Test content"
CONST_EMAIL = "email@example.com"
CONST_USERNAME = "user_name"
CONST_PASSWORD = "password"


class LikeTests(TestCase):
    def setUp(self):
        self._user = User.objects.create_user(
            "email@example.com", "user_name", "password"
        )

        self._post = Post.objects.create(
            title="Test title", content="Test content", author=self._user
        )

    def test_create_like(self):
        self._post.like(self._user)
        self.assertNotEqual(self._post.likes.count(), 0)

    def test_create_delete_like(self):
        self.test_create_like()
        self._post.unlike(self._user)
        self.assertEqual(self._post.likes.count(), 0)


class LikeAPITests(APITestCase):
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

        url = reverse("posts:list_create_posts")
        data = {"title": "Title", "content": "Content"}
        self.client.post(url, data, format="json")

    def test_like_post(self):
        url = reverse("likes:like_post", kwargs={"post_id": 1})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unlike_post(self):
        self.test_like_post()
        url = reverse("likes:unlike_post", kwargs={"post_id": 1})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_likes_post(self):
        self.test_like_post()
        url = reverse("likes:get_likes_post", kwargs={"post_id": 1})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
