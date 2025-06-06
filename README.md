# Dynamic-Website-Chatbot
A FastAPI-powered chatbot application that leverages LangChain, LangGraph, Large Language Models (LLMs), and vector embeddings to provide accurate, context-aware answers to user questions based on the content of any provided website URL

## Overview

This application provides a two-step process for creating intelligent chatbots from website content:

1. **Crawl Phase**: Extracts website content and creates a searchable vector database
2. **Chat Phase**: Enables natural language questions about the crawled content

## Features

- Asynchronous web crawling with crawl4ai
- Document chunking and vector embeddings with ChromaDB
- LangGraph workflow orchestration
- Azure OpenAI GPT-4o integration
- REST API with FastAPI

## Requirements

- Python >= 3.9
- Azure OpenAI API access
- Required Python packages (see installation section)

## Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd dynamic-website-chatbot
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a `secrets.env` file in the root directory:
```env
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT_4o=your_azure_openai_endpoint
AZURE_OPENAI_API_KEY_4o=your_azure_openai_api_key
AZURE_OPENAI_VERSION_4o=2024-02-15-preview

# LLM Settings
LLM_MODEL=gpt-4o
LLM_TEMPERATURE=0.1

# Vector Database
CHROMA_PERSIST_DIRECTORY=./chroma_db

# Crawler Settings
CRAWL_DEPTH=2
MAX_PAGES=50

# Document Processing
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# Retrieval Settings
TOP_K_RESULTS=4
```

## Usage

### Starting the Application

```bash
uvicorn app.main:app
```
##### No "--reload" with the uvicron cmd as it could lead to asyncio error on Crawl4AI.

The API will be available at `http://localhost:8000`

### API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.

## Workflow

### Crawl Workflow (LangGraph)

**Graph Structure**: 
- **Nodes**: crawl_website → process_content → create_vector_store
- **Edges**: Sequential flow with no branching
- **State**: CrawlState tracks URL, content, documents, and collection_name

**Node Execution**:
1. **crawl_website_node**: 
   - Input: website_url from state
   - Process: AsyncWebCrawler extracts content as markdown
   - Output: Updates state with website_content

2. **process_content_node**:
   - Input: website_content from state
   - Process: RecursiveCharacterTextSplitter chunks content into documents
   - Output: Updates state with documents array

3. **create_vector_store_node**:
   - Input: documents from state
   - Process: Creates ChromaDB collection with HuggingFace embeddings
   - Output: Updates state with vector_store and collection_name (MD5 hash of URL)

### Chat Workflow (LangGraph)

**Graph Structure**:
- **Nodes**: retrieve_documents → generate_response
- **Edges**: Sequential flow with no branching
- **State**: ChatState tracks collection_name, query, context, and answer

**Node Execution**:
1. **retrieve_documents_node**:
   - Input: collection_name and query from state
   - Process: Loads ChromaDB collection and performs similarity search
   - Output: Updates state with context (concatenated relevant documents)

2. **generate_response_node**:
   - Input: query and context from state
   - Process: Azure OpenAI generates response using structured prompt
   - Output: Updates state with final answer

## How the System Works

### Embedding Process

**What are Embeddings?**
Embeddings convert text into numerical vectors that capture semantic meaning. Similar texts produce similar number patterns, enabling semantic search beyond exact keyword matching.

**Creating Embeddings:**
1. Uses HuggingFace's "sentence-transformers/all-MiniLM-L6-v2" model
2. Converts each text chunk into 384-dimensional vectors
3. Example: "company founded in 2020" → `[0.23, -0.45, 0.78, ...]`

**Storage in ChromaDB:**
1. Website content is split into 1000-character chunks with 200-character overlap
2. Each chunk gets converted to embedding vectors
3. ChromaDB stores both original text and embeddings in collections
4. Collection names use MD5 hash of website URL for uniqueness

**Retrieval Process:**
1. User query gets converted to embedding using same model
2. ChromaDB performs cosine similarity search against stored embeddings
3. Returns top-k most semantically similar chunks
4. Combines retrieved chunks as context for LLM

**Why It Works:**
- Semantic understanding: "founded", "established", "started" have similar embeddings
- Context preservation: Related concepts cluster together numerically
- No exact word matching required - understands meaning and intent

## Architecture

**State Management**:
- `CrawlState`: Manages URL, content, documents, collection_name
- `ChatState`: Manages collection_name, query, context, answer

**Core Services**:
- `WebsiteCrawler`: Asynchronous web content extraction
- `DocumentProcessor`: Text chunking and document creation
- `VectorStore`: ChromaDB operations and embeddings
- `LLMService`: Azure OpenAI integration

**API Endpoints**:
- `POST /crawl`: Creates vector database from website URL
- `POST /chat`: Answers questions using collection content

## Development

### Project Structure
```
app/
├── config.py              # Configuration and settings
├── main.py               # FastAPI application entry point
├── models/
│   └── schemas.py        # Pydantic models for API
├── services/
│   ├── crawler.py        # Web crawling service
│   ├── document_processor.py  # Document processing
│   ├── vector_store.py   # Vector database operations
│   └── llm.py           # LLM service integration
└── graph/
    ├── state.py         # State management for workflows
    ├── nodes.py         # Individual workflow nodes
    └── workflow.py      # Workflow orchestration
```

### Key Dependencies

- **FastAPI**: Web framework for API endpoints
- **LangChain**: Document processing and LLM integration
- **LangGraph**: Workflow orchestration and state management
- **ChromaDB**: Vector database for embeddings
- **crawl4ai**: Asynchronous web crawling
- **HuggingFace**: Sentence transformers for embeddings
- **Azure OpenAI**: LLM for response generation

## Future Enhancements

- Support for multiple websites per collection
- Real-time content updates and re-crawling
- Advanced filtering and search capabilities
- User authentication and session management
- Batch processing for multiple URLs
- Custom embedding models and fine-tuning