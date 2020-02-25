from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Video(models.Model):
    """Model to represent Videos."""

    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    url = models.URLField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.modified_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} uploaded by {self.owner.username}'

    class Meta:
        verbose_name = 'Uploaded Video'
        verbose_name_plural = 'Uploaded Videos'


class VideoShare(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE,
                              related_name='shared')
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.video.title} shared with {self.shared_with.username}'

    class Meta:
        verbose_name = 'Video Share'
