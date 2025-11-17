"""RAG agent for document question answering."""

from crewai import Agent
from langchain_openai import ChatOpenAI
from typing import Optional
from loguru import logger
import sys
sys.path.append(str(__file__).rsplit('/', 3)[0])
from config.settings import OPENAI_API_KEY, OPENAI_MODEL
from src.tools.rag_tool import get_rag_tool
from src.utils.vector_store import VectorStore


def create_rag_agent(vector_store: Optional[VectorStore] = None) -> Agent:
    """
    Create an agent for answering questions based on uploaded documents.
    
    Args:
        vector_store: Optional VectorStore instance
        
    Returns:
        Agent configured for RAG-based Q&A
    """
    llm = ChatOpenAI(
        model=OPENAI_MODEL,
        temperature=0.3,
        openai_api_key=OPENAI_API_KEY
    )
    
    rag_tool = get_rag_tool(vector_store)
    
    agent = Agent(
        role="Document Q&A Specialist",
        goal="Answer questions accurately and comprehensively based on the uploaded course materials and assignment documents",
        backstory=(
            "You are an expert academic tutor with exceptional reading comprehension and synthesis abilities. "
            "You excel at understanding complex academic materials and explaining concepts clearly. "
            "You always cite your sources by referencing specific pages and documents. "
            "When answering questions, you provide detailed explanations with examples from the materials. "
            "You acknowledge when information is not available in the documents."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[rag_tool]
    )
    
    logger.info("Created RAG agent with document retrieval tool")
    return agent
