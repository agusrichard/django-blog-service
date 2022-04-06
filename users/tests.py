from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from django.db import IntegrityError
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from users.utils import (
    RELATIONSHIP_BLOCKED,
    RELATIONSHIP_FOLLOWING,
)

CONST_EMAIL = "email@example.com"
CONST_USERNAME = "user_name"
CONST_PASSWORD = "password"
CONST_NAMESPACE_ACTIVATE_URL = "users:activate_user"


class UserTests(TestCase):
    def test_new_superuser(self):
        db = get_user_model()
        new_superuser = db.objects.create_superuser(
            CONST_EMAIL, CONST_USERNAME, CONST_PASSWORD
        )
        self.assert_superuser_content(new_superuser)

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email=CONST_EMAIL,
                user_name=CONST_USERNAME,
                password=CONST_PASSWORD,
                is_superuser=False,
            )

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email=CONST_EMAIL,
                user_name=CONST_USERNAME,
                password=CONST_PASSWORD,
                is_staff=False,
            )

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email="",
                user_name=CONST_USERNAME,
                password=CONST_PASSWORD,
                is_superuser=True,
            )

    def test_new_user(self):
        db = get_user_model()
        new_user = db.objects.create_user(CONST_EMAIL, CONST_USERNAME, CONST_PASSWORD)
        new_user.save()
        self.assert_user_content(new_user)

        with self.assertRaises(ValueError):
            db.objects.create_user("", "user_name3", CONST_PASSWORD)

    def assert_superuser_content(self, user):
        self.assertEqual(user.email, CONST_EMAIL)
        self.assertEqual(user.user_name, CONST_USERNAME)
        self.assertEqual(str(user), CONST_EMAIL)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def assert_user_content(self, user):
        self.assertEqual(user.email, CONST_EMAIL)
        self.assertEqual(user.user_name, CONST_USERNAME)
        self.assertEqual(str(user), CONST_EMAIL)
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_user_notfound(self):
        db = get_user_model()
        with self.assertRaises(db.DoesNotExist):
            db.objects.get(email=CONST_EMAIL)

    def test_new_user_same_email(self):
        db = get_user_model()
        db.objects.create_user(CONST_EMAIL, "user_name1", "password1")
        with self.assertRaises(IntegrityError):
            db.objects.create_user(CONST_EMAIL, "user_name2", "password2")

    def test_new_user_same_user_name(self):
        db = get_user_model()
        db.objects.create_user("email1@example.com", "user_name1", "password1")
        with self.assertRaises(IntegrityError):
            db.objects.create_user("email2@example.com", "user_name1", "password2")

    def test_update_user(self):
        db = get_user_model()
        user = db.objects.create_user(CONST_EMAIL, CONST_USERNAME, CONST_PASSWORD)
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
        user = db.objects.create_user(CONST_EMAIL, CONST_USERNAME, CONST_PASSWORD)
        user.save()

        user.delete()
        with self.assertRaises(db.DoesNotExist):
            db.objects.get(email=CONST_EMAIL)

    def test_follow_user(self):
        user1, user2 = self.create_two_users()

        user1.follow(user2.id)
        user2.follow(user1.id)

        self.assertEqual(len(user1.get_relationships(status=RELATIONSHIP_FOLLOWING)), 1)
        self.assertEqual(len(user2.get_relationships(status=RELATIONSHIP_FOLLOWING)), 1)

    def test_block_user(self):
        user1, user2 = self.create_two_users()

        user1.block(user2.id)
        user2.block(user1.id)

        self.assertEqual(len(user1.get_relationships(status=RELATIONSHIP_BLOCKED)), 1)
        self.assertEqual(len(user2.get_relationships(status=RELATIONSHIP_BLOCKED)), 1)

    def create_two_users(self):
        db = get_user_model()
        user1 = db.objects.create_user(
            "email1@example.com", "user_name1", CONST_PASSWORD
        )
        user2 = db.objects.create_user(
            "email2@example.com", "user_name2", CONST_PASSWORD
        )
        user1.save()
        user2.save()

        return user1, user2


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

        url = reverse(CONST_NAMESPACE_ACTIVATE_URL)
        response_activate = self.client.post(url, data, format="json")
        self.assertEqual(response_activate.status_code, status.HTTP_200_OK)

    def test_login_user_api(self):
        response_create, data = self.create_user()
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)

        url = reverse(CONST_NAMESPACE_ACTIVATE_URL)
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

        url = reverse(CONST_NAMESPACE_ACTIVATE_URL)
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
