import logging
from fastapi import FastAPI, HTTPException
from app.models.schemas import ChatRequest, ChatResponse, CrawlRequest, CrawlResponse
from app.graph.workflow import create_chat_workflow, create_crawl_workflow
from app.config import settings

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

chat_workflow = create_chat_workflow()
crawl_workflow = create_crawl_workflow()

@app.post("/crawl", response_model=CrawlResponse)
async def crawl(request: CrawlRequest):
    try:
        result = await crawl_workflow.ainvoke({
            "website_url": request.website_url
        })
        
        return CrawlResponse(
            status="success",
            collection_name=result["collection_name"],
            content_length=len(result.get("website_content", "")))
    except Exception as e:
        logger.error(f"Error processing crawl request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Execute the chat workflow
        result = await chat_workflow.ainvoke({
            "collection_name": request.collection_name,
            "query": request.query
        })
        
        return ChatResponse(answer=result["answer"])
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)