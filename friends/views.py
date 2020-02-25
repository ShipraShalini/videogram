from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from common.jsonresponse import JSONResponse
from friends.friendrequesthandler import FriendRequestHandler
from friends.friendshiphandler import FriendshipHandler
from friends.userhandler import UserHandler


class CreateUser(APIView):
    
    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            UserHandler().create(
                username=data['username'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                password=data['password']
            )
        except KeyError:
            raise ValidationError('Please provide all fields.')
        return JSONResponse(
            data={'message': 'User Created.'},
            status=201
        )
        


class FriendRequestView(ModelViewSet):

    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        """Send friend request."""
        data = request.data
        try:
            FriendRequestHandler().add_friend(
                from_user=request.user,
                to_user_id=data['to_user_id'],
                to_user_username=data['to_user_username'],
                message=data['message'],
            )
        except KeyError:
            raise ValidationError('Please provide all fields.')
        return JSONResponse(
            data={'message': 'Friend Request Created.'},
            status=201
        )

    def list(self, request, *args, **kwargs):
        """Show friend requests."""
        friend_requests = FriendRequestHandler().show_friend_requests(
            user=request.user)
        return JSONResponse(
            data=friend_requests,
            status=200
        )

    def update(self, request, friend_req_id, *args, **kwargs):
        """Reject friend request and update rejected at."""
        FriendRequestHandler().reject(request.user, friend_req_id)
        return JSONResponse(
            data={'message': 'Friend Request Rejected.'},
            status=200
        )

    def destroy(self, request, friend_req_id, *args, **kwargs):
        """Accept friend request and delete it.."""
        FriendRequestHandler().accept(request.user, friend_req_id)
        return JSONResponse(
            data={'message': 'Friend Request Accepted.'},
            status=200
        )



class ListFriendshipView(APIView):
    
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        friendship_data = FriendshipHandler().list(request.user)
        return JSONResponse(
            data=friendship_data,
            status=200
        )


class DeleteFriendshipView(APIView):
    permission_classes = (IsAuthenticated,)
    def destroy(self, request, friendship_id, *args, **kwargs):
        FriendshipHandler().remove(request.user, friendship_id)
        return JSONResponse(
            data={'message': 'Friend Removed'},
            status=200
        )
    

class UserView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request, *args, **kwargs):
        data = UserHandler().retrieve(request.user)
        return JSONResponse(
            data=data,
            status=200
        )

    def put(self, request, *args, **kwargs):
        data = request.data
        try:
            data = UserHandler().modify(
                user=request.user,
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
            )
        except KeyError:
            raise ValidationError('Please provide all fields.')
        return JSONResponse(
            data=data,
            status=200
        )

    def delete(self, request, *args, **kwargs):
        UserHandler().delete(request.user)
        return JSONResponse(
            data={'message': 'User deleted.'},
            status=200
        )
