from pydantic import BaseModel, HttpUrl

class CrawlRequest(BaseModel):
    website_url: HttpUrl

class CrawlResponse(BaseModel):
    status: str
    collection_name: str
    content_length: int

class ChatRequest(BaseModel):
    collection_name: str
    query: str

class ChatResponse(BaseModel):
    answer: str