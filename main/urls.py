from django.urls import path, include

from .views import (
    HomePageView,
    InSystemUserProfileView,
    DifferentUserProfileView,
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

# User profile patterns
profile_urlpatterns = [
    path('update/', UserProfileUpdateView.as_view(), name='user_update'),
    path('delete/', UserDeleteView.as_view(), name='user_delete'),
    path('password_reset/complete/', UserPasswordResetCompleteView.as_view(),
         name='user_password_reset_complete'),
    path('password_reset/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(),
         name='user_password_reset_confirm'),
    path('password_reset/done/', UserPasswordResetDoneView.as_view(), name='user_password_reset_done'),
    path('password_reset/', UserPasswordResetView.as_view(), name='user_password_reset'),
]


# Authentication URL patterns
accounts_urlpatterns = [
    path('register/activate/<str:sign>/', activation_view, name='user_account_activate'),
    path('register/', UserRegisterView.as_view(), name='user_register'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),
    path('profile/', include(profile_urlpatterns)),
    path('my-profile/', InSystemUserProfileView.as_view(), name='user_profile'),
]


post_urlpatterns = [
    path('new/', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('<int:pk>/', user_post_detail_view, name='post_detail'),
    path('post/like/', post_like_view, name='post_like'),
    # path('post/<int:pk>/like/', post_like_view, name='post_like'),
]


app_name = 'main'
urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('accounts/', include(accounts_urlpatterns)),
    path('post/', include(post_urlpatterns)),
    path('user-<slug:username>/posts/', DifferentUserProfileView.as_view(), name='user_posts'),
    path('search/', search_redirect_view, name='search_redirect'),
    path('search-user/<str:content>/', UserSearchListView.as_view(), name='search')

]
''