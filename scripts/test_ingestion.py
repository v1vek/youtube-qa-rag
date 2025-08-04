import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
from ingest import downloader, transcriber, chunker
from config import CHUNK_DIR

url = input("Enter YouTube URL: ")

audio_path = downloader.download_audio(url)
print(f"Downloaded audio to: {audio_path}")

transcript_path = transcriber.transcribe_audio(audio_path)
print(f"Transcription saved to: {transcript_path}")

chunks = chunker.chunk_transcript(transcript_path)
print(f"Transcript chunked into {len(chunks)} parts.")

video_id = os.path.splitext(os.path.basename(audio_path))[0]
chunk_path = f"{CHUNK_DIR}/{video_id}.json"

os.makedirs(os.path.dirname(chunk_path), exist_ok=True)
with open(chunk_path, "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=2)

print(f"Chunks saved to: {chunk_path}")