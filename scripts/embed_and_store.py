import json
from vectorstore import embedder, db
from config import CHUNK_DIR

video_id = input("Enter video ID: ")
chunk_path = f"{CHUNK_DIR}/{video_id}.json"

with open(chunk_path, "r", encoding="utf-8") as f:
    chunks = json.load(f)

embedder.embed_chunks_if_needed(chunks, video_id)
