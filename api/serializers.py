from django.contrib.auth.models import Group
from main.models import User, Post

from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ('pk', 'title', 'content', 'picture', 'author', 'likes')


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, queryset=Post.objects.all())

    class Meta:
        model = User
        fields = ('pk', 'username', 'posts',)
