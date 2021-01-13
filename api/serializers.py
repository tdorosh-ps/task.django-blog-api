from django.core.paginator import Paginator
from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Post, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'body', 'created']


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['body']


class PostListSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    comments_count = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id', 'title', 'owner', 'comments_count', 'created', 'modified']

    def get_comments_count(self, obj):
        return obj.comments.count()


class PostCreateSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = Post
        fields = ['id', 'title', 'body']


class PostRetrieveSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    comments = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'owner', 'comments', 'created', 'modified']

    def get_comments(self, obj):
        page = self.context['request'].query_params.get('page', 1)
        per_page = self.context['request'].query_params.get('per_page', 5)
        paginator = Paginator(obj.comments.order_by('-created'), per_page)
        comments = paginator.get_page(page)
        serializer = CommentSerializer(comments, many=True)
        return {
            'data': serializer.data,
            'page': page,
            'per_page': per_page,
            'total': obj.comments.count(),
            'total_pages': comments.paginator.num_pages
        }