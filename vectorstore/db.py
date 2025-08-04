import chromadb

client = chromadb.PersistentClient(
    path="./chroma_db",
)

def get_or_create_collection(name: str):
    """
    Get or create a collection in the ChromaDB client.

    :param name: The name of the collection.
    :return: The collection object.
    """
    try:
        return client.get_or_create_collection(name)
    except Exception:
        return client.create_collection(name)
    
def store_chunks(chunks: list[dict], embeddings: list[list[float]], collection, video_id: str):
    """
    Store text chunks and their embeddings in the specified collection.

    :param chunks: A list of dictionaries containing text chunks.
    :param embeddings: A list of embeddings corresponding to the text chunks.
    :param collection: The ChromaDB collection to store the data in.
    :param video_id: The ID of the video associated with the chunks.
    """
    ids = [f"{video_id}_{i}" for i in range(len(chunks))]
    documents = [chunk['content'] for chunk in chunks]
    metadatas = [
        {
            "video_id": video_id,
            "start_time": chunk['start_time'],
            "end_time": chunk['end_time']
        }
        for chunk in chunks
    ]

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(f"Stored {len(chunks)} chunks in collection '{collection.name}' for video ID: {video_id}")