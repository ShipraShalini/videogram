from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import model_to_dict
from django.utils import timezone

from friends.models import Friendship
from videos.exceptions import UnauthorisedError
from videos.models import Video, VideoShare


class VideoHandler:

    def list(self, user):
        """List all the videos uploaded by the user."""
        return Video.objects.filter(owner=user).values(
            'id', 'title', 'uploaded_at'
        )

    def retrieve(self, user, video_id):
        """Retrieve details of the video."""
        video = self._get_by_id(user, video_id)
        data = model_to_dict(video)
        data['shared_with'] = VideoShareHandler.get_shared_with(video)
        return data

    def upload(self, user, title, description, url):
        """Upload a new video."""
        if Video.objects.filter(owner=user, url=url).exists():
            return ValidationError(
                'Video already exists. If you want to share it, use share API.'
            )

        return Video.objects.create(
            title=title,
            description=description,
            owner=user,
            url=url
        ).id

    def modify(self, user, video_id, title=None, description=None):
        """Modify the video."""
        if not (title or description):
            raise ValidationError('Nothing to update.')
        video = self._get_by_id(user, video_id)
        video.title = title or video.title
        video.description = description or video.description
        video.save()
        return model_to_dict(video)

    def delete(self, user, video_id):
        """Delete a video uploaded."""
        video = self._get_by_id(user, video_id)
        video.delete()

    @staticmethod
    def _get_by_id(user, video_id):
        """Get video instance by id."""
        try:
            video = Video.objects.get(video_id)
        except Video.DoesNotExist:
            raise ValidationError('No video with this id exists!')
        if video.owner != user:
            raise UnauthorisedError('Not authorized to view/modify the video.')
        return video


class VideoShareHandler:

    @staticmethod
    def get_shared_with(video):
        return VideoShare.objects.filter(
            video=video
        ).select_related(
            'shared_with'
        ).only(
            'shared_with__id',
            'shared_with__username',
            'shared_with__first_name',
            'shared_with__last_name'
        ).values_list(
            'shared_with__id',
            'shared_with__username',
            'shared_with__first_name',
            'shared_with__last_name'
        )

    def share(self, user, video_id, friend_ids):
        """Share videos with friends."""
        friend_users = self._get_validated_friends(user, friend_ids)
        video = VideoHandler._get_by_id(user, video_id)
        share_list = [VideoShare(video=video, shared_with=user)
                      for user in friend_users]
        VideoShare.objects.bulk_create(share_list)
        return self.get_shared_with(video)

    def unshare(self, user, video_id, friend_ids):
        """Unshare videos with friends."""
        friend_users = self._get_validated_friends(user, friend_ids)
        video = VideoHandler._get_by_id(user, video_id)
        VideoShare.objects.filter(
            video=video, shared_with__in=friend_users
        ).delete()
        return self.get_shared_with(video)

    def _get_validated_friends(self, user, friend_ids):
        """Check if friend list is acceptable."""
        friend_ids = friend_ids.replace(' ', '')
        try:
            friends = friend_ids.split(',')
        except (TypeError, ValueError):
            raise ValidationError(
                '`friend_ids` should be a comma separated string.'
            )
        if not friends:
            raise ValidationError(
                '`friend_ids` cannot be null.'
            )
        friends = Friendship.objects.filter(
            from_user=user, to_user_id__in=friends
        )
        if not friends.exists():
            raise ValidationError(
                '`friend_ids` does not have any valid friend.'
            )
        return friends.values_list('to_user', flat=True)