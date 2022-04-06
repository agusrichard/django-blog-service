from rest_framework import serializers
from django.contrib.auth import get_user_model

from posts.models import Post
from users.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=True)

    class Meta:
        model = Post
        fields = ("id", "title", "content", "created_at", "updated_at", "author")


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Post
        fields = ("id", "content", "created_at", "user")
