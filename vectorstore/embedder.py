from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_chunks(chunks: list[dict]) -> list[list[float]]:
    """
    Embed a list of text chunks using a pre-trained SentenceTransformer model.

    :param chunks: A list of dictionaries containing text chunks.
    :return: A list of embeddings corresponding to the text chunks.
    """
    texts = [chunk['content'] for chunk in chunks]
    return model.encode(texts).tolist()