from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    user_name = serializers.CharField(required=True)
    password = serializers.CharField(min_length=5, write_only=True)

    class Meta:
        model = User
        extra_kwargs = {"password": {"write_only": True}}
        fields = (
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
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.email = validated_data.get("email", instance.email)
        instance.user_name = validated_data.get("user_name", instance.user_name)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.bio = validated_data.get("bio", instance.bio)
        instance.save()
        return instance
