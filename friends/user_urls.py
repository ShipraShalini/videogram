from django.urls import path

from rest_framework.routers import DefaultRouter

from friends.views import (CreateUser, FriendRequestView,
                           ListFriendshipView, UserView, DeleteFriendshipView)

app_name = 'friends'

urlpatterns = [
    path('signup', CreateUser.as_view(), name='create_user'),
    path('signin', CreateUser.as_view(), name='signin'),
    path('user', UserView.as_view(), name='user'),
]
