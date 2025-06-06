from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from app.config import settings

class LLMService:
    def __init__(self):
        self.llm = AzureChatOpenAI(
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT_4o,
            api_key=settings.AZURE_OPENAI_API_KEY_4o,
            api_version=settings.AZURE_OPENAI_VERSION_4o,
            deployment_name=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE
        )
        self.prompt = PromptTemplate.from_template(
            """You are a helpful assistant that answers questions about websites.
            
            Context information from the website:
            {context}
            
            User question: {query}
            
            Provide a helpful, accurate, and concise answer based on the context information:"""
        )
    
    async def generate_response(self, query, context):
        """Generate a response using the LLM with the new Runnable interface"""
        print(f"Generating response for query: {query} with context: {context}")
        chain = (
            {"query": RunnablePassthrough(), "context": RunnablePassthrough()} 
            | self.prompt
            | self.llm
        )
        result = await chain.ainvoke({"query": query, "context": context})
        print(f"LLM response: {result.content}")
        return result.content