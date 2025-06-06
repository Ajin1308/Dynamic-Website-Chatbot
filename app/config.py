import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv("secrets.env")

class Settings:
    # API settings
    APP_NAME = "Dynamic Website Chatbot"
    APP_VERSION = "1.0.0"
    
    # OpenAI settings
    AZURE_OPENAI_ENDPOINT_4o = os.getenv("AZURE_OPENAI_ENDPOINT_4o")
    AZURE_OPENAI_API_KEY_4o = os.getenv("AZURE_OPENAI_API_KEY_4o")
    AZURE_OPENAI_VERSION_4o = os.getenv("AZURE_OPENAI_VERSION_4o")
    
    # LLM settings
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o")
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.1"))

    # Vector DB settings
    CHROMA_PERSIST_DIRECTORY = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")
    
    # Crawler settings
    CRAWL_DEPTH = int(os.getenv("CRAWL_DEPTH", "2"))
    MAX_PAGES = int(os.getenv("MAX_PAGES", "50"))
    
    # Document processing settings
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
    
    # Retrieval settings
    TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", "4"))

# Create a settings instance
settings = Settings()