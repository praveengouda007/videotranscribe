from django.db import models

class Video(models.Model):
    """
    Model representing a video file.

    Attributes:
        title (str): The title of the video.
        file (FileField): The video file.
        uploaded_at (DateTimeField): Timestamp when the video was uploaded.
        is_processed (bool): Indicates if subtitles have been processed.
    """
    title: str = models.CharField(max_length=255)
    file: models.FileField = models.FileField(upload_to='videos/')
    uploaded_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    is_processed: bool = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title


class Subtitle(models.Model):
    """
    Model representing subtitles for a video.

    Attributes:
        video (ForeignKey): The video associated with the subtitle.
        language (str): The language of the subtitle.
        timestamp (float): The timestamp of the subtitle in seconds.
        text (str): The subtitle text.
    """
    video: Video = models.ForeignKey(Video, related_name='subtitles', on_delete=models.CASCADE)
    language: str = models.CharField(max_length=20, default='en')
    timestamp: float = models.FloatField()
    text: str = models.TextField()

    def __str__(self) -> str:
        return f"{self.text} @ {self.timestamp}"
