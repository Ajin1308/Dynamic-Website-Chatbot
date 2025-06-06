from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from app.config import settings

class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP
        )
    
    def process_content(self, content: str, metadata: dict = None):
        """Process and chunk website content"""
        if metadata is None:
            metadata = {}
        
        documents = [Document(page_content=content, metadata=metadata)]
        chunks = self.text_splitter.split_documents(documents)
        return chunks