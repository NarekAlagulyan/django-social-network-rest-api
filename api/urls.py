from django.urls import include
from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, UserViewSet


router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'users', UserViewSet)


app_name = 'api'
urlpatterns = [
    path('', include(router.urls)),
]

