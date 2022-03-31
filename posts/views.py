from rest_framework import status
from rest_framework.response import Response
from django.forms.models import model_to_dict
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from posts.models import Post
from posts.serializers import PostSerializer


class PostListCreateView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        title = request.data.get("title")
        if title == "":
            return Response(
                {"message": "Title is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        content = request.data.get("content")
        if content == "":
            return Response(
                {"message": "Content is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        new_post = Post.objects.create(
            title=request.data.get("title"),
            content=request.data.get("content"),
            author=request.user,
        )
        new_post.save()

        serializer = PostSerializer(new_post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def patch(self, request, pk):
        post = Post.objects.get(pk=pk)
        if post.author != request.user:
            return Response(
                {"message": "You are not allowed to edit this post"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = PostSerializer(post, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
