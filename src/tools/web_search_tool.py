"""Web search tool using SerperAPI."""

from crewai_tools import SerperDevTool
from loguru import logger
import sys
sys.path.append(str(__file__).rsplit('/', 3)[0])
from config.settings import SERPER_API_KEY


def get_search_tool():
    """
    Get configured SerperAPI search tool.
    
    Returns:
        SerperDevTool instance
    """
    try:
        search_tool = SerperDevTool(
            search_url="https://google.serper.dev/search",
            n_results=10,
        )
        
        logger.info("Initialized SerperAPI search tool")
        return search_tool
        
    except Exception as e:
        logger.error(f"Error initializing search tool: {str(e)}")
        raise


# Create a singleton instance
search_tool = get_search_tool()
