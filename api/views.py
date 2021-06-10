from rest_framework import decorators, status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, ListAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.decorators import api_view
from rest_framework.renderers import StaticHTMLRenderer
from rest_framework import viewsets
from rest_framework.decorators import action

from django.shortcuts import get_object_or_404
from django.views.generic import UpdateView


from main.models import User


from .serializers import PostSerializer, UserSerializer
from .permissions import IsAuthorOrReadOnly
from main.models import Post


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    @action(detail=True, renderer_classes=[StaticHTMLRenderer])
    def title(self, request, *args, **kwargs):
        post = self.get_object()
        return Response(post.title)

    def perform_create(self, serializer):
        serializer.save(self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

