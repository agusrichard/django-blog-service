from rest_framework import status
from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from users.utils import RelationshipActions
from users.serializers import UserSerializer, CustomTokenObtainPairSerializer


class UserCreateView(CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(
                {"message": "Wrong email or password"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserRetrieveUpdateView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class FollowUserView(CreateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            request.user.follow(request.data["user_id"])
            return Response(status=status.HTTP_200_OK)
        except get_user_model().DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class UserActivateView(CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        try:
            email = request.data.get("email")
            password = request.data.get("password")

            user = get_user_model().objects.get(email=email)
            if not check_password(password, user.password):
                raise IntegrityError

            user.is_active = True
            user.save()

            return Response(None, status=status.HTTP_200_OK)
        except IntegrityError:
            return Response(
                {"message": "Wrong email or password"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserRelationshipView(CreateAPIView):
    def post(self, request):
        try:
            action = request.data["action"]
            if action == RelationshipActions.FOLLOW:
                request.user.follow(request.data["user_id"])
            elif action == RelationshipActions.UNFOLLOW:
                request.user.unfollow(request.data["user_id"])
            elif action == RelationshipActions.BLOCK:
                request.user.block(request.data["user_id"])
            elif action == RelationshipActions.UNBLOCK:
                request.user.unblock(request.data["user_id"])
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            return Response(status=status.HTTP_204_NO_CONTENT)
        except get_user_model().DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
