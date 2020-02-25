from django.urls import path

from rest_framework.routers import DefaultRouter

from friends.views import (CreateUser, FriendRequestView,
                           ListFriendshipView, UserView, DeleteFriendshipView)

app_name = 'friends'


urlpatterns = [
    path('<int:friendship_id>/delete', DeleteFriendshipView.as_view(),
         name='delete-friendship'),
    path('list', ListFriendshipView.as_view(), name='list-friends'),
    path('friendrequest/', FriendRequestView.as_view({
        'get': 'list',
        'post': 'create'
    }), name='friendrequest'),
    path('friendrequest/<int:friend_req_id>', FriendRequestView.as_view({
        'put': 'update',
        'delete': 'destroy'
    }), name='friendrequest'),
]

urlpatterns = [
    path('signup', CreateUser.as_view(), name='create_user'),
    path('signin', CreateUser.as_view(), name='create_user'),
    path('user', UserView.as_view(), name='user'),
]