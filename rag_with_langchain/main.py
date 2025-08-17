import argparse
from ingest import downloader, transcriber, chunker
from vectorstore import vectorstore
from utils import extract_video_id

def main(video_id: str, query: str, top_k: int = 2):
    print(f"📺 Processing video: {video_id}")

    # Download audio
    audio_path = downloader.download_audio(video_id)

    # Transcribe audio
    transcript_path = transcriber.transcribe_audio(audio_path)

    # Chunk transcript
    docs = chunker.chunk_transcript(transcript_path, video_id, return_doc=True)

    # Embed and store chunks
    chroma_store = vectorstore.get_vectorstore()
    vectorstore.add_documents(chroma_store, video_id, docs)

    retriever = vectorstore.get_retriever(chroma_store, video_id, top_k)
    qa_chain = vectorstore.build_qa_chain(retriever)
    
    result = qa_chain.invoke(query)
    print("\n💬 Answer:")
    print(result["result"])

    # Sources
    print("\n📚 Sources:")
    for source in result["source_documents"]:
        video_id = source.metadata.get("video_id")
        start = source.metadata.get("start_time")
        print(f"- [{start}s](https://www.youtube.com/watch?v={video_id}&t={start}s): {source.page_content}")


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