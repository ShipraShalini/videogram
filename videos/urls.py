from django.urls import path


from videos.views import VideoView, ShareVideoView

app_name = 'videos'


urlpatterns = [

    path('share/<int:video_id>/', ShareVideoView.as_view(), name='share'),
    path('<int:video_id>/', VideoView.as_view(
        {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='video-modify'),
    path('', VideoView.as_view({'post': 'create', 'get': 'list', }),
         name='video'),
]
