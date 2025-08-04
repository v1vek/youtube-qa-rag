from sentence_transformers import SentenceTransformer
import chromadb
from config import CHROMA_COLLECTION_NAME

model = SentenceTransformer('all-MiniLM-L6-v2')

client = chromadb.PersistentClient(
    path="./chroma_db",
)
collection = client.get_or_create_collection(CHROMA_COLLECTION_NAME)

def retrieve_relevant_chunks(query: str, video_id: str, top_k = 5) -> list[dict]:
    """
    Retrieve relevant chunks from the ChromaDB collection based on a query.

    :param query: The search query.
    :param video_id: The ID of the video to filter results.
    :param top_k: The number of top results to return.
    :return: A list of dictionaries containing relevant chunks and their metadata.
    """
    query_embeddings = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embeddings],
        n_results=top_k,
        where={"video_id": video_id}
    )

    chunks = []
    documents = results.get('documents')
    metadatas = results.get('metadatas')
    if documents and metadatas and documents[0] is not None and metadatas[0] is not None:
        for doc, metadata in zip(documents[0], metadatas[0]):
            chunks.append({
                "content": doc,
                "start_time": metadata['start_time'],
                "end_time": metadata['end_time'],
                "video_id": metadata['video_id']
            })

    return chunks