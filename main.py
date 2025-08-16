import argparse
from urllib.parse import quote
from ingest import downloader, transcriber, chunker
from vectorstore import embedder
from rag import retriever, answerer
from utils import extract_video_id

def main(video_id: str, query: str, top_k: int = 2):
    print(f"📺 Processing video: {video_id}")

    # Download audio
    audio_path = downloader.download_audio(video_id)

    # Transcribe audio
    transcript_path = transcriber.transcribe_audio(audio_path)

    # Chunk transcript
    chunks = chunker.chunk_transcript(transcript_path, video_id)

    # Embed and store chunks
    embedder.embed_chunks_if_needed(chunks, video_id)

    # Retrieve relevant chunks
    retrieved_chunks = retriever.retrieve_relevant_chunks(query, video_id, top_k=top_k)
    print(f"Retrieved {len(retrieved_chunks)} relevant chunks.")

    if not retrieved_chunks:
        print("❌ No relevant information found in the transcript for your query.")
        print("💡 Try rephrasing your question or verifying the video content.")
        return

    # Generate answer
    answer = answerer.generate_answer(query, retrieved_chunks)
    print("\n💬 Answer:")
    print(answer)

    # Sources
    print("\n📚 Sources:")
    for chunk in retrieved_chunks:
        ts = int(float(chunk["start_time"]))
        snippet = chunk["content"][:100].strip() + "..."
        link = f"https://www.youtube.com/watch?v={chunk['video_id']}&t={ts}s"
        print(f"- [{ts}s]({link}): {snippet}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="YouTube video URL")
    parser.add_argument("--query", required=True, help="Question to ask")
    parser.add_argument("--top-k", type=int, default=2, help="Top K chunks to retrieve")
    args = parser.parse_args()

    video_id = extract_video_id(args.url)
    if not video_id:
        raise ValueError("Invalid YouTube URL: unable to extract video ID")

    main(video_id, args.query, args.top_k)