from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from django.db import IntegrityError
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model


class UserTests(TestCase):
    def test_new_superuser(self):
        db = get_user_model()
        new_superuser = db.objects.create_superuser(
            "email@example.com", "user_name", "password"
        )
        self.assert_superuser_content(new_superuser)

        with self.assertRaises(ValueError):
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
        new_user.save()
        self.assert_user_content(new_user)

        with self.assertRaises(ValueError):
            db.objects.create_user("", "user_name3", "password")

    def assert_superuser_content(self, user):
        self.assertEqual(user.email, "email@example.com")
        self.assertEqual(user.user_name, "user_name")
        self.assertEqual(str(user), "<User: email@example.com>")
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def assert_user_content(self, user):
        self.assertEqual(user.email, "email@example.com")
        self.assertEqual(user.user_name, "user_name")
        self.assertEqual(str(user), "<User: email@example.com>")
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_user_notfound(self):
        db = get_user_model()
        with self.assertRaises(db.DoesNotExist):
            db.objects.get(email="email@example.com")

    def test_new_user_same_email(self):
        db = get_user_model()
        db.objects.create_user("email@example.com", "user_name1", "password1")
        with self.assertRaises(IntegrityError):
            db.objects.create_user("email@example.com", "user_name2", "password2")

    def test_new_user_same_user_name(self):
        db = get_user_model()
        db.objects.create_user("email1@example.com", "user_name1", "password1")
        with self.assertRaises(IntegrityError):
            db.objects.create_user("email2@example.com", "user_name1", "password2")

    def test_update_user(self):
        db = get_user_model()
        user = db.objects.create_user("email@example.com", "user_name", "password")
        self.assert_user_content(user)

        user.first_name = "first_name"
        user.last_name = "last_name"
        user.bio = "bio"
        user.save()

        self.assertEqual(user.first_name, "first_name")
        self.assertEqual(user.last_name, "last_name")
        self.assertEqual(user.bio, "bio")

    def test_delete_user(self):
        db = get_user_model()
        user = db.objects.create_user("email@example.com", "user_name", "password")
        user.save()

        user.delete()
        with self.assertRaises(db.DoesNotExist):
            db.objects.get(email="email@example.com")


class UserAPITests(APITestCase):
    def create_user(self):
        url = reverse("users:create_user")
        data = {
            "email": "test_user@example.com",
            "user_name": "test_user",
            "password": "test_user",
        }

        return self.client.post(url, data, format="json"), data

    def test_create_user_api(self):
        response, _ = self.create_user()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("email"), "test_user@example.com")
        self.assertEqual(response.data.get("user_name"), "test_user")
        self.assertEqual(response.data.get("first_name"), "")
        self.assertEqual(response.data.get("last_name"), "")
        self.assertEqual(response.data.get("bio"), "")
        self.assertFalse(response.data.get("is_active"))
        self.assertFalse(response.data.get("is_staff"))

    def test_activate_user_api(self):
        response_create, data = self.create_user()
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)

        url = reverse("users:activate_user")
        response_activate = self.client.post(url, data, format="json")
        self.assertEqual(response_activate.status_code, status.HTTP_200_OK)

    def test_login_user_api(self):
        response_create, data = self.create_user()
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)

        url = reverse("users:activate_user")
        response_activate = self.client.post(url, data, format="json")
        self.assertEqual(response_activate.status_code, status.HTTP_200_OK)

        url = reverse("users:token_obtain_pair")
        response_login = self.client.post(url, data, format="json")
        self.assertEqual(response_login.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in response_login.data)
        self.assertTrue("refresh" in response_login.data)

    def test_get_profile_api(self):
        response_create, data = self.create_user()
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)

        url = reverse("users:activate_user")
        response_activate = self.client.post(url, data, format="json")
        self.assertEqual(response_activate.status_code, status.HTTP_200_OK)

        url = reverse("users:token_obtain_pair")
        response_login = self.client.post(url, data, format="json")
        self.assertEqual(response_login.status_code, status.HTTP_200_OK)

        url = reverse("users:retrieve_user")
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + response_login.data["access"]
        )
        response_profile = self.client.get(url)
        self.assertEqual(response_profile.status_code, status.HTTP_200_OK)
