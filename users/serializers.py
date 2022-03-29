from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        extra_kwargs = {"password": {"write_only": True}}
        fields = (
            "id",
            "email",
            "user_name",
            "first_name",
            "last_name",
            "password",
            "date_joined",
            "bio",
            "is_staff",
            "is_active",
        )

    def create(self, validated_data):
        if validated_data.get("email") is None:
            raise serializers.ValidationError("email is required")

        if validated_data.get("user_name") is None:
            raise serializers.ValidationError("user_name is required")

        if validated_data.get("password") is None:
            raise serializers.ValidationError("password is required")

        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.bio = validated_data.get("bio", instance.bio)
        instance.save()
        return instance


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        user.last_login = timezone.now()
        user.save()
        token = super().get_token(user)

        return token
