from django.shortcuts import get_object_or_404
from rest_framework import generics

from .models import Post
from .serializers import PostListSerializer, PostCreateSerializer, PostRetrieveSerializer, \
    CommentCreateSerializer


class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.order_by('-created')[:5]
    serializer_class = PostListSerializer


class PostCreateAPIView(generics.CreateAPIView):
    serializer_class = PostCreateSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostRetrieveSerializer
    lookup_url_kwarg = 'post_id'


class CommentCreateAPIView(generics.CreateAPIView):
    serializer_class = CommentCreateSerializer

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(owner=self.request.user, post=post)