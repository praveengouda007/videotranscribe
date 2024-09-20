from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Video
from vidsub_app.tasks import process_video


def video_upload(request) -> JsonResponse:
    """
    View to upload a new video.

    Args:
        request: The HTTP request object.

    Returns:
        JsonResponse: Redirects to the video list on successful upload.
    """
    if request.method == 'POST':
        video_file = request.FILES.get('video')
        title = request.POST.get('title')
        video_instance = Video.objects.create(title=title, file=video_file)
        process_video.delay(video_instance.id)
        return redirect('video_list')
    return render(request, 'video_upload.html')


def video_list(request) -> JsonResponse:
    """
    View to list all videos ordered by upload date.

    Args:
        request: The HTTP request object.

    Returns:
        JsonResponse: Renders a list of videos.
    """
    videos = Video.objects.all().order_by('-uploaded_at')
    latest_video = videos.first()
    return render(request, 'video_list.html', {'videos': videos, 'latest_video': latest_video})


def video_detail(request, pk: int) -> JsonResponse:
    """
    View to get details of a specific video.

    Args:
        request: The HTTP request object.
        pk (int): Primary key of the video.

    Returns:
        JsonResponse: Renders details of the video and its subtitles.
    """
    video = get_object_or_404(Video, pk=pk)
    subtitles = video.subtitles.all()
    return render(request, 'video_detail.html', {'video': video, 'subtitles': subtitles})



def video_subtitles(request, video_id: int) -> JsonResponse:
    """
    View to get subtitles for a specific video.

    Args:
        request: The HTTP request object.
        video_id (int): ID of the video.

    Returns:
        JsonResponse: List of subtitles associated with the video.
    """
    video = get_object_or_404(Video, id=video_id)
    subtitles = video.subtitles.all()

    subtitle_list = [
        {"timestamp": subtitle.timestamp, "text": subtitle.text}
        for subtitle in subtitles
    ]

    return JsonResponse({"subtitles": subtitle_list})

def search_subtitles(request, video_id: int) -> JsonResponse:
    """
    View to search for subtitles containing a specific phrase.

    Args:
        request: The HTTP request object.
        video_id (int): ID of the video.

    Returns:
        JsonResponse: Timestamp and text of the matching subtitle or error message.
    """
    phrase = request.GET.get('phrase', '')
    video = get_object_or_404(Video, id=video_id)
    matching_subtitle = video.subtitles.filter(text__icontains=phrase).first()

    if matching_subtitle:
        return JsonResponse({
            'timestamp': matching_subtitle.timestamp,
            'text': matching_subtitle.text
        })
    return JsonResponse({"error": "Phrase not found"}, status=404)
