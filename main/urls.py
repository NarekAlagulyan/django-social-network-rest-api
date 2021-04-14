from django.urls import path

from .views import (
    HomePageView,
    UserProfileView,
    UserRegisterView,
    UserProfileUpdateView,
    UserDeleteView,
    UserLoginView,
    UserLogoutView,
    UserPasswordResetView,
    UserPasswordResetDoneView,
    UserPasswordResetConfirmView,
    UserPasswordResetCompleteView,
    activation_view,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    user_post_detail_view,
    post_like_view,
    UserSearchListView,
    search_redirect_view,
)

app_name = 'main'
urlpatterns = [
    path('', HomePageView.as_view(), name='home'),

    # authentication
    path('accounts/register/activate/<str:sign>/', activation_view, name='user_account_activate'),
    path('accounts/register/', UserRegisterView.as_view(), name='user_register'),
    path('accounts/login/', UserLoginView.as_view(), name='user_login'),
    path('accounts/logout/', UserLogoutView.as_view(), name='user_logout'),
    path('accounts/profile/update/', UserProfileUpdateView.as_view(), name='user_update'),
    path('accounts/profile/delete/', UserDeleteView.as_view(), name='user_delete'),
    path('accounts/profile/password_reset/complete/', UserPasswordResetCompleteView.as_view(),
         name='user_password_reset_complete'),
    path('accounts/profile/password_reset/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(),
         name='user_password_reset_confirm'),
    path('accounts/profile/password_reset/done/', UserPasswordResetDoneView.as_view(), name='user_password_reset_done'),
    path('accounts/profile/password_reset/', UserPasswordResetView.as_view(), name='user_password_reset'),
    path('accounts/my-profile/', UserProfileView.as_view(), name='user_profile'),

    # post
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:pk>/', user_post_detail_view, name='post_detail'),

    # path('post/<int:pk>/like/', post_like_view, name='post_like'),
    path('post/like/', post_like_view, name='post_like'),

    path('<str:username>/posts/', UserPostListView.as_view(), name='user_posts'),
    path('search/', search_redirect_view, name='search_redirect'),
    path('search-user/<str:content>/', UserSearchListView.as_view(), name='search')

]
