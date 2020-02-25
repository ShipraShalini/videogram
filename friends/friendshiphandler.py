from django.db import transaction
from rest_framework.exceptions import ValidationError

from friends.models import Friendship


class FriendshipHandler:

    def list(self, user):
        return Friendship.objects.filter(
            to_user=user
        ).select_related(
            'from_user'
        ).values(
            'id',
            'from_user__username',
            'from_user__first_name',
            'from_user__last_name',
            'created_at'
        )

    def remove(self, user, friendship_id):
        friendship = self._get_friendship_by_id(user, friendship_id)
        rev_friendship = Friendship.objects.get(
            to_user=friendship.from_user,
            from_user=friendship.to_user
        )

        with transaction.atomic():
            friendship.delete()
            rev_friendship.delete()

    def _get_friendship_by_id(self, user, friendship_id,
                              err_message='Friendship Does not exist.'):
        """Get user by id."""
        try:
            return Friendship.objects.get(
                id=friendship_id, to_user=user
            )
        except Friendship.DoesNotExist:
            raise ValidationError(err_message)