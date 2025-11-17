"""Assignment detail extraction agent using GPT-4o."""

from crewai import Agent
from langchain_openai import ChatOpenAI
from loguru import logger
import sys
sys.path.append(str(__file__).rsplit('/', 3)[0])
from config.settings import OPENAI_API_KEY, OPENAI_MODEL


def create_extraction_agent() -> Agent:
    """
    Create an agent for extracting assignment details from text.
    
    Returns:
        Agent configured for detail extraction
    """
    llm = ChatOpenAI(
        model=OPENAI_MODEL,
        temperature=0.1,
        openai_api_key=OPENAI_API_KEY
    )
    
    agent = Agent(
        role="Assignment Details Analyzer",
        goal="Extract and structure key information from assignment documents including topic, course name, requirements, and important details",
        backstory=(
            "You are an expert academic analyst with years of experience reviewing course assignments. "
            "You excel at identifying critical information such as assignment topics, course names, "
            "learning objectives, requirements, deliverables, and evaluation criteria. "
            "You always extract information accurately and present it in a clear, structured format."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    logger.info("Created extraction agent")
    return agent
