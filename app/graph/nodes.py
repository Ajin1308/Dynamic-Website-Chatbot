from langchain_chroma import Chroma 
from app.services.crawler import WebsiteCrawler
from app.services.document_processor import DocumentProcessor
from app.services.vector_store import VectorStore
from app.services.llm import LLMService
from app.config import settings
import hashlib
import asyncio

# Create instances
crawler = WebsiteCrawler()
processor = DocumentProcessor()
vector_store = VectorStore()
llm_service = LLMService()


async def crawl_website_node(state):
    """Node for crawling website content with proper async handling"""
    try:
        url = str(state["website_url"])
        content = await crawler.crawl_website(url)  # Properly await the coroutine
        return {"website_content": content}
    except Exception as e:
        raise Exception(f"Crawling failed: {str(e)}")

def process_content_node(state):
    """Node for processing website content"""
    content = state["website_content"]
    url = str(state["website_url"])
    
    metadata = {"source": url}
    documents = processor.process_content(content, metadata)
    return {"documents": documents}

def create_vector_store_node(state):
    """Node for creating vector store"""
    documents = state["documents"]
    url = str(state["website_url"])
    
    collection_name = hashlib.md5(url.encode()).hexdigest()
    db = vector_store.create_vector_store_sync(documents, collection_name)
    return {"vector_store": db, "collection_name": collection_name}

def retrieve_documents_node(state):
    """Node for retrieving relevant documents"""
    query = state["query"]
    collection_name = state["collection_name"]
    
    # Load existing vector store
    db = Chroma(
        collection_name=collection_name,
        embedding_function=vector_store.embeddings,
        persist_directory=settings.CHROMA_PERSIST_DIRECTORY
    )
    
    docs = vector_store.query_vector_store_sync(db, query, k=settings.TOP_K_RESULTS)
    context = "\n\n".join([doc.page_content for doc in docs])
    return {"context": context}

async def generate_response_node(state):
    """Node for generating response using LLM"""
    query = state["query"]
    context = state["context"]
    
    try:
        result = await llm_service.generate_response(query, context)
        return {"answer": result}
    except Exception as e:
        return {"answer": f"Error generating response: {str(e)}"}
