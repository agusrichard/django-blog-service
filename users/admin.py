from django.contrib import admin
from django.forms import TextInput, Textarea
from django.contrib.auth.admin import UserAdmin

from users.models import User


class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ("email", "user_name", "first_name", "last_name")
    list_filter = (
        "email",
        "user_name",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
    )
    ordering = ("-date_joined",)
    list_display = (
        "email",
        "user_name",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
    )
    fieldsets = (
        (
            None,
            {"fields": ("email", "user_name", "first_name", "last_name")},
        ),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
        ("Personal", {"fields": ("bio",)}),
    )
    formfield_overrides = {
        User.bio: {"widget": Textarea(attrs={"rows": 10, "cols": 40})},
    }
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "user_name",
                    "first_name",
                    "last_name",
                    "bio",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )


# Register your models here.
admin.site.register(User, UserAdminConfig)
