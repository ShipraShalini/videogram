from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from common.jsonresponse import JSONResponse

from videos.videohandler import VideoHandler, VideoShareHandler


class VideoView(ModelViewSet):

    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            video_id = VideoHandler().upload(
                user=request.user,
                title=data['title'],
                description=data['description'],
                url=data['url'],
            )
        except KeyError:
            raise ValidationError('Please provide all fields.')
        return JSONResponse(
            data={'video_id': video_id},
            status=201
        )

    def list(self, request, *args, **kwargs):
        video_list = VideoHandler().list(user=request.user)
        return JSONResponse(
            data={'video_list': video_list},
            status=200
        )

    def retrieve(self, request, video_id, *args, **kwargs):
        video_details = VideoHandler().retrieve(request.user, video_id)
        return JSONResponse(
            data={'video_details': video_details},
            status=200
        )

    def destroy(self, request, video_id, *args, **kwargs):
        VideoHandler().delete(request.user, video_id)
        return JSONResponse(status=200)

    def update(self, request, video_id, *args, **kwargs):
        data = request.data
        try:
            video_details = VideoHandler().modify(
                user=request.user,
                video_id=video_id,
                title=data['title'],
                description=data['description'],
            )
        except KeyError:
            raise ValidationError('Please provide all fields.')
        return JSONResponse(
            data={'video_details': video_details},
            status=200
        )


class ShareVideoView(APIView):
    """API class to share videos."""

    permission_classes = (IsAuthenticated,)

    def post(self, request, video_id, *args, **kwargs):
        data = request.data
        video_details = VideoShareHandler().share(
            user=request.user,
            video_id=video_id,
            friend_ids=data.get('friend_ids'),
        )
        return JSONResponse(
            data={'video_details': video_details},
            status=200
        )

    def destroy(self, request, video_id, *args, **kwargs):
        friend_ids = request.data.get('friend_ids')
        if not friend_ids:
            raise ValidationError(
                'Please provide Friend id to stop sharing videos.'
            )
        video_details = VideoShareHandler().unshare(
            user=request.user,
            video_id=video_id,
            friend_ids=friend_ids
        )
        return JSONResponse(
            data={'video_details': video_details},
            status=200
        )
