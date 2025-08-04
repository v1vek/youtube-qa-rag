import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
from vectorstore import embedder, db

video_id = input("Enter video ID: ")
chunk_path = f"data/chunks/{video_id}.json"

with open(chunk_path, "r", encoding="utf-8") as f:
    chunks = json.load(f)

embeddings = embedder.embed_chunks(chunks)

collection = db.get_or_create_collection("video_chunks")
db.store_chunks(chunks, embeddings, collection, video_id)