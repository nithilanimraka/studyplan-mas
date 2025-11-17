"""RAG question-answering crew with web enhancement."""

from crewai import Crew, Task, Process
from typing import Dict, Optional
from loguru import logger
import sys
sys.path.append(str(__file__).rsplit('/', 3)[0])
from src.agents.web_rag_agent import create_web_rag_agent
from src.utils.vector_store import VectorStore


class RAGCrew:
    """Crew for answering questions using RAG and web search."""
    
    def __init__(self, vector_store: Optional[VectorStore] = None):
        """
        Initialize the RAG crew with agents.
        
        Args:
            vector_store: Optional VectorStore instance
        """
        self.vector_store = vector_store or VectorStore()
        self.web_rag_agent = create_web_rag_agent(self.vector_store)
        
        logger.info("Initialized RAGCrew with web-enhanced agent")
    
    def create_task(self, question: str) -> Task:
        """
        Create a task for answering a question.
        
        Args:
            question: User's question
            
        Returns:
            Task object
        """
        task = Task(
            description=(
                f"Answer the following question comprehensively:\n\n"
                f"{question}\n\n"
                f"Follow this process:\n"
                f"1. First, search the uploaded course materials for relevant information\n"
                f"2. Then, perform a web search to find additional context, examples, or current information\n"
                f"3. Synthesize both sources into a comprehensive answer\n\n"
                f"Your answer should:\n"
                f"- Start with information from the course materials (if available)\n"
                f"- Enhance with relevant web research\n"
                f"- Cite sources clearly:\n"
                f"  * For course materials: mention page numbers and document names\n"
                f"  * For web sources: include URLs and source names\n"
                f"- Be well-organized with clear sections\n"
                f"- Include examples and explanations\n"
                f"- Acknowledge if certain information is not available\n\n"
                f"Format your answer in markdown with headers, lists, and emphasis where appropriate."
            ),
            expected_output=(
                "A comprehensive answer that combines information from course materials and web research, "
                "with clear citations, examples, and explanations. Use markdown formatting."
            ),
            agent=self.web_rag_agent
        )
        
        return task
    
    def answer_question(self, question: str) -> Dict:
        """
        Answer a question using RAG and web search.
        
        Args:
            question: User's question
            
        Returns:
            Dictionary with answer and metadata
        """
        try:
            logger.info(f"Processing question: {question[:50]}...")
            
            # Create task
            task = self.create_task(question)
            
            # Create crew
            crew = Crew(
                agents=[self.web_rag_agent],
                tasks=[task],
                process=Process.sequential,
                verbose=True
            )
            
            # Execute crew
            result = crew.kickoff()
            
            logger.info("Question answered successfully")
            
            return {
                "success": True,
                "answer": result,
                "question": question
            }
            
        except Exception as e:
            logger.error(f"Error answering question: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "question": question
            }
