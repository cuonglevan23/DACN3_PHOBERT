import os
from googleapiclient.discovery import build

API_KEY = ''

def get_youtube_service():
    """Khởi tạo dịch vụ YouTube API."""
    return build('youtube', 'v3', developerKey=API_KEY)

def extract_video_id(video_url):
    """Trích xuất video ID từ URL."""
    if 'youtube.com/watch?v=' in video_url:
        return video_url.split('v=')[1].split('&')[0]
    elif 'youtu.be/' in video_url:
        return video_url.split('youtu.be/')[1].split('?')[0]
    else:
        raise ValueError("Invalid YouTube URL")

def get_video_comments(video_url, max_comments=100):
    """Lấy nhiều bình luận từ video YouTube."""
    video_id = extract_video_id(video_url)
    youtube = get_youtube_service()

    comments = []
    request = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        textFormat='plainText',
        maxResults=100  # Lấy tối đa 100 bình luận mỗi lần gọi
    )

    while request and len(comments) < max_comments:
        response = request.execute()

        for item in response.get('items', []):
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)
            if len(comments) >= max_comments:
                break

        request = youtube.commentThreads().list_next(request, response)  # Lấy trang tiếp theo (nếu có)

    return comments

def get_video_info(video_url):
    """Lấy thông tin chi tiết từ video YouTube bao gồm statistics và thumbnail."""
    video_id = extract_video_id(video_url)
    youtube = get_youtube_service()

    request = youtube.videos().list(
        part='snippet,statistics',
        id=video_id
    )
    response = request.execute()

    video_info = response.get('items', [])[0]
    statistics = video_info['statistics']
    snippet = video_info['snippet']

    return {
        'title': snippet['title'],
        'view_count': statistics.get('viewCount'),
        'comment_count': statistics.get('commentCount'),
        'thumbnail_url': snippet['thumbnails']['high']['url']  # Lấy thumbnail chất lượng cao
    }