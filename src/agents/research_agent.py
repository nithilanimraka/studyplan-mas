"""Research agent for web searching."""

from crewai import Agent
from langchain_openai import ChatOpenAI
from loguru import logger
import sys
sys.path.append(str(__file__).rsplit('/', 3)[0])
from config.settings import OPENAI_API_KEY, OPENAI_MODEL
from src.tools.web_search_tool import search_tool


def create_research_agent() -> Agent:
    """
    Create an agent for web research using SerperAPI.
    
    Returns:
        Agent configured for web research
    """
    llm = ChatOpenAI(
        model=OPENAI_MODEL,
        temperature=0.7,
        openai_api_key=OPENAI_API_KEY
    )
    
    agent = Agent(
        role="Web Research Specialist",
        goal="Find high-quality educational resources, study materials, tutorials, and learning paths related to the assignment topic",
        backstory=(
            "You are a skilled research librarian and educational resource curator with expertise in finding "
            "the best online learning materials. You know how to identify credible sources, comprehensive tutorials, "
            "video courses, documentation, and academic resources. You understand how students learn and can find "
            "resources suitable for different learning styles and skill levels."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[search_tool]
    )
    
    logger.info("Created research agent with SerperAPI tool")
    return agent
