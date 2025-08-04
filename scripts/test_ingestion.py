import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ingest import downloader

url = input("Enter YouTube URL: ")

audio_path = downloader.download_audio(url)
print(f"Downloaded audio to: {audio_path}")