import uuid

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

from .managers import CustomUserManager

class User(AbstractBaseUser, PermissionsMixin):

    ADMIN = 1
    MODERATOR = 2
    NORMAL = 3

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (MODERATOR, 'Manager'),
        (NORMAL, 'Normal')
    )

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, verbose_name='Public Identifier')
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=100)
    full_name = models.CharField(max_length=100, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True, default=3)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.EmailField()
    created_date = models.DateTimeField(default=timezone.now)
    modified_by = models.EmailField()
    modified_date = models.DateTimeField(default=timezone.now)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'username'

    objects = CustomUserManager()

    def __str__(self):
        return self.email