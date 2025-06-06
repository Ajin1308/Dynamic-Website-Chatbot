import chromadb
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from app.config import settings

class VectorStore:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
    
    def create_vector_store_sync(self, documents, collection_name):
        """Create a new vector store for the website - synchronous version"""
        return Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            collection_name=collection_name,
            persist_directory=settings.CHROMA_PERSIST_DIRECTORY
        )
    
    def query_vector_store_sync(self, vector_store, query, k=None):
        """Query the vector store for relevant documents"""
        return vector_store.similarity_search(query, k=k)
    
    async def create_vector_store(self, documents, collection_name):
        """Create a new vector store for the website"""
        return Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            collection_name=collection_name,
            persist_directory=settings.CHROMA_PERSIST_DIRECTORY
        )