import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
from vectorstore import embedder, db
from config import CHUNK_DIR, CHROMA_COLLECTION_NAME

video_id = input("Enter video ID: ")
chunk_path = f"{CHUNK_DIR}/{video_id}.json"

with open(chunk_path, "r", encoding="utf-8") as f:
    chunks = json.load(f)

embeddings = embedder.embed_chunks(chunks)

collection = db.get_or_create_collection(CHROMA_COLLECTION_NAME)
db.store_chunks(chunks, embeddings, collection, video_id)