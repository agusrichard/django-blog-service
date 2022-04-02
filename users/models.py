from django.db import IntegrityError, models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from users.managers import UserManager
from users.utils import (
    RELATIONSHIP_BLOCKED,
    RELATIONSHIP_FOLLOWING,
    RELATIONSHIP_STATUSES,
)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    bio = models.TextField(_("about"), blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    relationships = models.ManyToManyField(
        "self", through="Relationship", symmetrical=False, related_name="related_to"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["user_name"]

    objects = UserManager()

    class Meta:
        ordering = ["date_joined"]

    def __str__(self):
        return f"<User: {self.email}>"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def add_relationship(self, user, status):
        relationship, created = Relationship.objects.get_or_create(
            from_user=self, to_user=user, status=status
        )
        if not created:
            raise IntegrityError("Relationship already exists")
        return relationship

    def remove_relationship(self, user):
        Relationship.objects.filter(from_user=self, to_user=user).delete()

    def follow(self, user_id):
        user = User.objects.get(id=user_id)
        return self.add_relationship(user, RELATIONSHIP_FOLLOWING)

    def unfollow(self, user_id):
        user = User.objects.get(id=user_id)
        self.remove_relationship(user)

    def block(self, user_id):
        user = User.objects.get(id=user_id)
        return self.add_relationship(user, RELATIONSHIP_BLOCKED)

    def unblock(self, user_id):
        self.unfollow(user_id)

    def get_relationships(self, status):
        return self.relationships.filter(
            following__status=status, following__from_user=self
        )

    def get_related_to(self, status):
        return self.related_to.filter(followers__status=status, followers__to_user=self)

    def get_following(self):
        return self.get_relationships(status=RELATIONSHIP_FOLLOWING)

    def get_followers(self):
        return self.get_related_to(status=RELATIONSHIP_FOLLOWING)


class Relationship(models.Model):
    from_user = models.ForeignKey(
        User, related_name="followers", on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        User, related_name="following", on_delete=models.CASCADE
    )
    status = models.IntegerField(choices=RELATIONSHIP_STATUSES)

    class Meta:
        unique_together = ("from_user", "to_user")

    def __str__(self):
        if self.status == RELATIONSHIP_FOLLOWING:
            return f"{self.from_user} follow {self.to_user}"
        else:
            return f"{self.from_user} block {self.to_user}"
