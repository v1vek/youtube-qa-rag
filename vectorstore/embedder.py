from sentence_transformers import SentenceTransformer
from vectorstore import db
from config import CHROMA_COLLECTION_NAME

model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_chunks_if_needed(chunks: list[dict], video_id: str, force: bool = False):
    """
    Embed a list of text chunks using a pre-trained SentenceTransformer model.

    :param chunks: A list of dictionaries containing text chunks.
    :return: A list of embeddings corresponding to the text chunks.
    """
    collection = db.get_or_create_collection(CHROMA_COLLECTION_NAME)

    if not force:
        existing_embeddings = collection.query(
            query_texts=["placeholder"],
            n_results=1,
            where={"video_id": video_id}
        )

        if existing_embeddings["ids"] and existing_embeddings["ids"][0]:
            print(f"Using existing embeddings for video ID: {video_id}")
            return existing_embeddings["embeddings"]

    texts = [chunk['content'] for chunk in chunks]
    embeddings = model.encode(texts).tolist()
    db.store_chunks(chunks, embeddings, collection, video_id)
    print(f"Embeddings stored for video ID: {video_id}")