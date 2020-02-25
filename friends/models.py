from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Friendship(models.Model):
    """Model to represent Friendships."""

    to_user = models.ForeignKey(User, models.CASCADE, related_name='friends')
    from_user = models.ForeignKey(User, models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'User {self.to_user_id} is friends with {self.from_user_id}'

    def save(self, *args, **kwargs):
        # Ensure users can't be friends with themselves
        if self.to_user == self.from_user:
            raise ValidationError('Users cannot be friends with themselves.')
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Friend'
        verbose_name_plural = 'Friends'
        unique_together = ('from_user', 'to_user')


class FriendRequest(models.Model):
    """Model to represent friend requests."""

    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='friendship_requests_sent',
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='friendship_requests_received',
    )

    message = models.TextField('Message', blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    rejected_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.from_user_id

    class Meta:
        verbose_name = 'Friendship Request'
        verbose_name_plural = 'Friendship Requests'
        unique_together = ('from_user', 'to_user')

