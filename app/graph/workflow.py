from langgraph.graph import StateGraph
from app.graph.state import CrawlState, ChatState
from app.graph.nodes import (
    crawl_website_node,
    process_content_node,
    create_vector_store_node,
    retrieve_documents_node,
    generate_response_node
)

def create_crawl_workflow():
    """Create a workflow for the crawling process"""
    workflow = StateGraph(CrawlState)
    
    workflow.add_node("crawl_website", crawl_website_node)
    workflow.add_node("process_content", process_content_node)
    workflow.add_node("create_vector_store", create_vector_store_node)
    
    workflow.add_edge("crawl_website", "process_content")
    workflow.add_edge("process_content", "create_vector_store")
    
    workflow.set_entry_point("crawl_website")
    workflow.set_finish_point("create_vector_store")
    
    return workflow.compile()

def create_chat_workflow():
    """Create a workflow for the chat process"""
    workflow = StateGraph(ChatState)
    
    workflow.add_node("retrieve_documents", retrieve_documents_node)
    workflow.add_node("generate_response", generate_response_node)
    
    workflow.add_edge("retrieve_documents", "generate_response")
    
    workflow.set_entry_point("retrieve_documents")
    workflow.set_finish_point("generate_response")
    
    return workflow.compile()