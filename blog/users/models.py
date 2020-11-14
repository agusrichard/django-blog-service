import uuid

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

from .managers import CustomUserManager

class User(AbstractBaseUser, PermissionsMixin):

    # ADMIN = 1
    # MODERATOR = 2

    # ROLE_CHOICES = (

    # )

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, verbose_name='Public Identifier')
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100, blank=True)
    # role = 
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.EmailField()
    created_date = models.DateTimeField(default=timezone.now)
    modified_by = models.EmailField()
    modified_date = models.DateTimeField(default=timezone.now)

    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email