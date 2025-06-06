from typing import Any, List, TypedDict
from langchain.schema import Document

class CrawlState(TypedDict, total=False):
    website_url: str
    website_content: str
    documents: List[Document]
    collection_name: str

class ChatState(TypedDict, total=False):
    collection_name: str
    query: str
    vector_store: Any
    context: str
    answer: str