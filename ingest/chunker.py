import re

def chunk_transcript(transcript_path: str, chunk_size: int = 500) -> list:
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