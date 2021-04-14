from django.urls import path

from .views import (
    user_api_view,
    post_api_view,
    comment_api_view,
    most_liked_post_api_view,
    user_biggest_amount_of_post_view,
)

app_name = 'api'

urlpatterns = [
    path('main/users-biggest-amount-of-posts/', user_biggest_amount_of_post_view),
    path('main/users/', user_api_view),
    path('main/posts/', post_api_view),
    path('main/most-liked-posts/', most_liked_post_api_view),
    path('main/comments/', comment_api_view),
]
