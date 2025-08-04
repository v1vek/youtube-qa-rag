import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from rag import retriever, answerer

video_id = input("Enter video ID: ")
query = input("Enter your query: ")

chunks = retriever.retrieve_relevant_chunks(query, video_id, top_k=2)
print(f"Retrieved {len(chunks)} relevant chunks.")
# print("Chunks: ", chunks)

top_chunk = chunks[0]
video_id = top_chunk["video_id"]
start_time = int(float(top_chunk["start_time"]))

youtube_link = f"https://www.youtube.com/watch?v={video_id}&t={start_time}s"

answer = answerer.generate_answer(query, chunks)
print(f"Generated answer: {answer}")
print(f"\n🔗 [Watch the relevant part of the video here]({youtube_link})")
