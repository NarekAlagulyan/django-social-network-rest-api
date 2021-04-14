from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models.aggregates import Count

from main.models import User, Post, Comment, MostPostUserProxy, MostLikedPostProxy
from .serializers import UserSerializer, PostSerializer, CommentSerializer
# Create your views here.


@api_view(['GET'])
def user_api_view(request):
    if request.method == 'GET':
        users = User.objects.filter(is_active=True)[:5]
        serialize = UserSerializer(users, many=True)
        return Response(serialize.data)


@api_view(['GET'])
def user_biggest_amount_of_post_view(request):
    if request.method == 'GET':
        users = MostPostUserProxy.objects.all()
        serialize = UserSerializer(users, many=True)
        return Response(serialize.data)


@api_view(['GET'])
def post_api_view(request):
    if request.method == 'GET':
        posts = Post.objects.all()[:30]
        serialize = PostSerializer(posts, many=True)
        return Response(serialize.data)


@api_view(['GET'])
def most_liked_post_api_view(request):
    if request.method == 'GET':
        posts = MostLikedPostProxy.objects.all()
        serialize = PostSerializer(posts, many=True)
        return Response(serialize.data)


@api_view(['GET'])
def comment_api_view(request):
    if request.method == 'GET':
        comments = Comment.objects.filter()[:3]
        serialize = CommentSerializer(comments, many=True)
        return Response(serialize.data)

