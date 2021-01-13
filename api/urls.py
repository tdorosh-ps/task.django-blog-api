from django.urls import path
from rest_framework.authtoken import views as auth_views

from . import views

urlpatterns = [
    path('post/list/', views.PostListAPIView.as_view(), name='post-list'),
    path('post/create/', views.PostCreateAPIView.as_view(), name='post-create'),
    path('post/<int:post_id>/', views.PostRetrieveAPIView.as_view(), name='post-retrieve'),
    path('post/<int:post_id>/add_comment/', views.CommentCreateAPIView.as_view(), name='post-add-comment'),
    path('api-token-auth/', auth_views.obtain_auth_token, name='blog-auth')
]