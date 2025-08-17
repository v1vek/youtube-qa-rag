from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

from config import CHROMA_COLLECTION_NAME, OPENAI_MODEL

def get_vectorstore(persist_directory="./chroma_db"):
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = Chroma(
        collection_name=CHROMA_COLLECTION_NAME,
        embedding_function=embedding_model,
        persist_directory="./chroma_db"
    )
    return vectorstore

def add_documents(vectorstore, video_id: str, docs, force=False):
    existing = vectorstore.get(where={"video_id": video_id})
    if existing["ids"]:
        print(f"Using existing embeddings for video ID: {video_id}")
    else:
        print(f"Storing new embeddings for video ID: {video_id}")
        vectorstore.add_documents(docs)

def get_retriever(vectorstore, video_id: str, top_k: int = 2):
    retriever = vectorstore.as_retriever(
        search_kwargs={ "k": top_k, "filter": {"video_id": video_id} },
        search_type="similarity"
    )
    return retriever

def build_qa_chain(retriever):
    llm = ChatOpenAI(model=OPENAI_MODEL)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        return_source_documents=True
    )    
    return qa_chain

