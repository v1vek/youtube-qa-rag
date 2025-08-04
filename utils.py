from urllib.parse import urlparse, parse_qs

def extract_video_id(url: str) -> str:
    """
    Extracts the YouTube video ID from a given URL.
    Supports URLs like:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    """
    parsed = urlparse(url)

    # Handle youtu.be links
    if parsed.hostname in ("youtu.be",):
        return parsed.path.lstrip("/")

    # Handle youtube.com/watch?v=...
    if parsed.hostname in ("www.youtube.com", "youtube.com"):
        query = parse_qs(parsed.query)
        video_id = query.get("v", [None])[0]
        if video_id is None:
            raise ValueError("Invalid YouTube URL: missing video ID")
        return video_id

    raise ValueError("Invalid YouTube URL")
