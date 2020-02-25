from django.urls import path


from videos.views import VideoView, ShareVideoView, UnShareVideoView

app_name = 'videos'


urlpatterns = [
    path('/', VideoView.as_view(), name='info'),
    path('share/<int:video_id>/', ShareVideoView.as_view(), name='share'),
    path('unshareshare/<int:video_id>/', UnShareVideoView.as_view(),
         name='unshare')
]
