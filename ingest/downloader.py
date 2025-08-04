import yt_dlp
from pathlib import Path
from config import AUDIO_DIR

def download_audio(url: str, output_dir = AUDIO_DIR) -> str:
    """
    Download audio from a given URL and save it to the specified output path.

    :param url: The URL of the audio to download.
    :param output_dir: The path where the downloaded audio will be saved.
    """

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
        info = ydl.extract_info(url, download=False)
        if info is None:
            raise ValueError(f"Could not extract info for URL: {url}")
        video_id = info["id"]
        filename = f"{video_id}.mp3"
        output_path = Path(output_dir) / filename

    if output_path.exists():
        print(f"File already exists: {output_path}")
        return str(output_path)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f"{output_dir}/%(id)s.%(ext)s",
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"Downloading audio for video ID: {video_id}")
        ydl.download([url])

    return str(output_path)