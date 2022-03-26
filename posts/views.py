from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from posts.models import Post
from posts.serializers import PostSerializer


class PostListCreateView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
