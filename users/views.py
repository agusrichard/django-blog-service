from rest_framework import status
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework_simplejwt.views import TokenObtainPairView

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


class UserRetrieveView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
