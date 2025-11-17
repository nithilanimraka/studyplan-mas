"""Planning agent for creating study plans."""

from crewai import Agent
from langchain_openai import ChatOpenAI
from loguru import logger
import sys
sys.path.append(str(__file__).rsplit('/', 3)[0])
from config.settings import OPENAI_API_KEY, OPENAI_MODEL


def create_planning_agent() -> Agent:
    """
    Create an agent for generating personalized study plans.
    
    Returns:
        Agent configured for study planning
    """
    llm = ChatOpenAI(
        model=OPENAI_MODEL,
        temperature=0.5,
        openai_api_key=OPENAI_API_KEY
    )
    
    agent = Agent(
        role="Study Plan Architect",
        goal="Create detailed, actionable study plans with clear milestones, time allocations, and learning objectives based on the deadline and assignment requirements",
        backstory=(
            "You are an expert educational consultant and learning strategist with a PhD in Educational Psychology. "
            "You specialize in creating personalized study plans that maximize learning efficiency and retention. "
            "You understand how to break down complex topics into manageable chunks, set realistic milestones, "
            "and allocate time effectively. You consider cognitive load, spaced repetition, and active learning principles. "
            "Your study plans are always practical, motivating, and designed for success."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    logger.info("Created planning agent")
    return agent
