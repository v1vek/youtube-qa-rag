import os
import json
import re

from langchain.schema import Document
from config import CHUNK_DIR

def chunk_transcript(transcript_path: str, video_id: str, return_doc: bool = False, chunk_size: int = 500) -> list:
    """
    Chunk a transcript into smaller segments.

    :param transcript: The full transcript text.
    :param chunk_size: The maximum size of each chunk.
    :return: A list of text chunks.
    """
    chunk_path = os.path.join(CHUNK_DIR, f"{video_id}.json")
    if os.path.exists(chunk_path):
        print(f"Chunks already exist for video ID: {video_id}")
        with open(chunk_path, "r", encoding="utf-8") as f:
            chunks = json.load(f)
    else:
        chunks = _chunk_transcript(transcript_path, chunk_size)
        os.makedirs(CHUNK_DIR, exist_ok=True)
        with open(chunk_path, "w", encoding="utf-8") as f:
            json.dump(chunks, f, indent=2)
        print(f"Chunks created and saved to: {chunk_path}")
    
    if return_doc:
        return _json_to_documents(chunks, video_id)
    else:
        return chunks

def _chunk_transcript(transcript_path: str, chunk_size: int = 500) -> list:
    """
    Chunk a transcript into smaller segments.

    :param transcript: The full transcript text.
    :param chunk_size: The maximum size of each chunk.
    :return: A list of text chunks.
    """
    with open(transcript_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    chunks = []
    current_chunk = []
    start_time = None
    end = None

    for line in lines:
        match = re.match(r"\[(.*?) - (.*?)\] (.+)", line.strip())
        if match:
            start, end, text = match.groups()
            if not start_time:
                start_time = start

            current_chunk.append(text)
            combined = " ".join(current_chunk)

            if len(combined) >= chunk_size:
                chunks.append({
                    "content": combined,
                    "start_time": start_time,
                    "end_time": end
                })
                current_chunk = []
                start_time = None

    if current_chunk:
        chunks.append({
            "content": " ".join(current_chunk),
            "start_time": start_time,
            "end_time": end
        })

    return chunks

def _json_to_documents(chunks:list, video_id: str) -> list:
    """
    Convert stored JSON chunks into LangChain Document objects.
    """
    return [
        Document(
            page_content=chunk["content"],
            metadata={
                "video_id": video_id,
                "start_time": chunk["start_time"],
                "end_time": chunk["end_time"]
            }
        ) for chunk in chunks
    ]