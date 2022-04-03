from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from posts.models import Post
from users.serializers import UserSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def like_post(request):
    try:
        post_id = request.GET.get("post_id")
        post = Post.objects.get(id=post_id)
        post.like(request.user)
        return Response(status=status.HTTP_200_OK)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_likes(request, post_id):
    try:
        print("post_id", post_id)
        post = Post.objects.get(id=post_id)
        likes = post.get_likes()
        serializer = UserSerializer(likes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
