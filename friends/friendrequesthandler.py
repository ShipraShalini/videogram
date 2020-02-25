from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from friends.exceptions import AlreadyFriendsError, AlreadyExistsError
from friends.models import Friendship, FriendRequest


class FriendRequestHandler:

    def are_friends(self, user1, user2):
        """Are these two users friends?"""
        return Friendship.objects.get(to_user=user1, from_user=user2).exists()

    def can_request_send(self, from_user, to_user):
        """ Checks if a request was sent """
        if from_user == to_user:
            return False

        return not FriendRequest.objects.filter(
            from_user=from_user, to_user=to_user
        ).exists()

    def add_friend(self, from_user, to_user_id, to_user_username, message=None):
        """Create a friendship request."""
        to_user = self._get_user_by_id(
            to_user_id,
            err_message=f'User with {to_user_username} does not exist.'
        )
        if from_user == to_user:
            raise ValidationError('Users cannot be friends with themselves.')

        if self.are_friends(from_user, to_user):
            raise AlreadyFriendsError('Users are already friends.')

        if self.can_request_send(from_user, to_user):
            raise AlreadyExistsError('Friendship already requested')

        message = message or ''

        FriendRequest.objects.create(
            from_user=from_user, to_user=to_user, message=message
        )

    def remove_friend(self, from_user, to_user):
        """Destroy a friendship relationship."""
        qs = (Friendship.objects.filter(
            Q(to_user=to_user, from_user=from_user)|
            Q(to_user=from_user, from_user=to_user)
        ).distinct().all())
        if qs.exists():
            qs.delete()
            return True

    def accept(self, user, friend_req_id):
        """Accept this friendship request."""
        friend_req = self.get_friend_request_by_id(user, friend_req_id)
        friends = [
            Friendship(
                from_user=friend_req.from_user, to_user=friend_req.to_user
            ),
            Friendship(
                from_user=friend_req.to_user, to_user=friend_req.from_user
            )
        ]
        with transaction.atomic():
            Friendship.objects.bulk_create(friends)

            # Delete any reverse requests
            FriendRequest.objects.filter(
                from_user=friend_req.to_user, to_user=friend_req.from_user
            ).delete()
            friend_req.delete()

    def reject(self, user, friend_req_id):
        """Reject this friendship request."""
        friend_req = self.get_friend_request_by_id(user, friend_req_id)
        friend_req.rejected = timezone.now()
        friend_req.save()

    def show_friend_requests(self, user):
        """List friendship request."""
        return FriendRequest.objects.filter(
            from_user=user, rejected__is_null=True
        ).select_related('from_user').values(
            'id',
            'from_user__username',
            'from_user__first_name',
            'from_user__last_name',
            'message',
            'created_at'
        )

    def _get_user_by_id(self, user_id, err_message='User Does not exist.'):
        """Get user by id."""
        try:
            return User.objects.get(id=user_id, is_active=True)
        except User.DoesNotExist:
            raise ValidationError(err_message)

    def get_friend_request_by_id(self, to_user, req_id):
        try:
            return FriendRequest.objects.get(id=req_id, to_user=to_user)
        except FriendRequest.DoesNotExist:
            raise ValidationError(f'Friend request doesn\'t exist for '
                                  f'{to_user.username}')
