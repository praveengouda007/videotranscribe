import os
import subprocess
from typing import Optional
from celery import shared_task
from django.conf import settings
from .models import Video, Subtitle


@shared_task
def process_video(video_id: int) -> None:
    """
    Processes a video by extracting subtitles using ffmpeg.

    Args:
        video_id (int): The ID of the video to process.
    """
    video = Video.objects.get(id=video_id)
    video_path = os.path.join(settings.MEDIA_ROOT, video.file.name)

    # Subtitle extraction logic
    subtitle_path = f'{os.path.splitext(video_path)[0]}.srt'
    command = [
        'ffmpeg', '-i', video_path, '-map', '0:s:0', subtitle_path
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Parse .srt file and save subtitles in DB
    parse_and_save_subtitles(video, subtitle_path)

    video.is_processed = True
    video.save()


def parse_and_save_subtitles(video: Video, subtitle_path: str) -> None:
    """
    Parses the .srt file and saves subtitles into the database.

    Args:
        video (Video): The Video instance to associate subtitles with.
        subtitle_path (str): The path to the .srt file.
    """
    with open(subtitle_path, 'r') as f:
        lines = f.readlines()

    timestamp: Optional[float] = None
    subtitle_text: str = ""

    for line in lines:
        if '-->' in line:
            timestamp = line.split(' --> ')[0]
            timestamp = convert_srt_timestamp_to_seconds(timestamp)
        elif line.strip() == "":
            if timestamp is not None and subtitle_text:
                Subtitle.objects.create(
                    video=video,
                    timestamp=timestamp,
                    text=subtitle_text.strip()
                )
                timestamp = None
                subtitle_text = ""
        else:
            subtitle_text += line.strip() + " "


def convert_srt_timestamp_to_seconds(timestamp: str) -> float:
    """
    Converts a timestamp from .srt format to seconds.

    Args:
        timestamp (str): The timestamp string in .srt format.

    Returns:
        float: The equivalent time in seconds.
    """
    h, m, s = map(float, timestamp.replace(',', '.').split(':'))
    return h * 3600 + m * 60 + s
