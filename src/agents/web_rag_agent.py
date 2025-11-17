"""Web-enhanced RAG agent for intelligent Q&A with web search."""

from crewai import Agent
from langchain_openai import ChatOpenAI
from typing import Optional
from loguru import logger
import sys
sys.path.append(str(__file__).rsplit('/', 3)[0])
from config.settings import OPENAI_API_KEY, OPENAI_MODEL
from src.tools.rag_tool import get_rag_tool
from src.tools.web_search_tool import search_tool
from src.utils.vector_store import VectorStore


def create_web_rag_agent(vector_store: Optional[VectorStore] = None) -> Agent:
    """
    Create an agent for answering questions using both documents and web search.
    
    Args:
        vector_store: Optional VectorStore instance
        
    Returns:
        Agent configured for web-enhanced RAG Q&A
    """
    llm = ChatOpenAI(
        model=OPENAI_MODEL,
        temperature=0.4,
        openai_api_key=OPENAI_API_KEY
    )
    
    rag_tool = get_rag_tool(vector_store)
    
    agent = Agent(
        role="Enhanced Research Assistant",
        goal="Provide comprehensive answers by combining information from uploaded documents with current web research to give complete, accurate, and contextually rich responses",
        backstory=(
            "You are a brilliant research assistant with access to both course materials and the internet. "
            "You have a unique ability to synthesize information from multiple sources - both the uploaded documents "
            "and current web resources. You always start by searching the course materials for relevant information, "
            "then enhance your answers with additional context, examples, and current information from web searches. "
            "You clearly distinguish between information from the course materials and supplementary web research. "
            "You provide citations for both document sources (with page numbers) and web sources (with URLs). "
            "Your answers are comprehensive, well-organized, and educational."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[rag_tool, search_tool]
    )
    
    logger.info("Created web-enhanced RAG agent with document retrieval and web search tools")
    return agent
