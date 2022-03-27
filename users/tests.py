from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model


class UserTests(TestCase):
    def test_new_superuser(self):
        db = get_user_model()
        new_superuser = db.objects.create_superuser(
            "email@example.com", "user_name", "password"
        )
        self.assertEqual(new_superuser.email, "email@example.com")
        self.assertEqual(new_superuser.user_name, "user_name")
        self.assertEqual(str(new_superuser), "<User: email@example.com>")
        self.assertTrue(new_superuser.is_active)
        self.assertTrue(new_superuser.is_staff)
        self.assertTrue(new_superuser.is_superuser)

        with self.assertRaises(ValueError) as err:
            db.objects.create_superuser(
                email="email@example.com",
                user_name="user_name",
                password="password",
                is_superuser=False,
            )

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email="email@example.com",
                user_name="user_name",
                password="password",
                is_staff=False,
            )

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email="",
                user_name="user_name",
                password="password",
                is_superuser=True,
            )

    def test_new_user(self):
        db = get_user_model()
        new_user = db.objects.create_user("email@example.com", "user_name", "password")
        self.assertEqual(new_user.email, "email@example.com")
        self.assertEqual(new_user.user_name, "user_name")
        self.assertEqual(str(new_user), "<User: email@example.com>")
        self.assertFalse(new_user.is_active)
        self.assertFalse(new_user.is_staff)
        self.assertFalse(new_user.is_superuser)

        with self.assertRaises(ValueError):
            db.objects.create_user("", "user_name3", "password")


class UserAPITests(APITestCase):
    def test_user_api(self):
        url = reverse("users:create_user")
        data = {
            "email": "test_user@example.com",
            "user_name": "test_user",
            "password": "test_user",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("email"), "test_user@example.com")
        self.assertEqual(response.data.get("user_name"), "test_user")
        self.assertEqual(response.data.get("first_name"), "")
        self.assertEqual(response.data.get("last_name"), "")
        self.assertEqual(response.data.get("bio"), "")
        self.assertFalse(response.data.get("is_active"))
        self.assertFalse(response.data.get("is_staff"))
