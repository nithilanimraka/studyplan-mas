"""RAG tool for document retrieval and question answering."""

from crewai.tools import BaseTool
from typing import Type, Optional
from pydantic import BaseModel, Field
from loguru import logger
import sys
sys.path.append(str(__file__).rsplit('/', 3)[0])
from src.utils.vector_store import VectorStore


class RAGQueryInput(BaseModel):
    """Input schema for RAGTool."""
    query: str = Field(..., description="The question or query to search for in the documents")


class RAGTool(BaseTool):
    """Tool for retrieving relevant information from uploaded documents."""
    
    name: str = "Document Search and Retrieval"
    description: str = (
        "Searches through uploaded course materials and assignment documents to find relevant information. "
        "Use this tool to answer questions based on the content of uploaded PDFs or text. "
        "Provide a clear question or query as input."
    )
    args_schema: Type[BaseModel] = RAGQueryInput
    vector_store: Optional[VectorStore] = None
    
    def __init__(self, vector_store: Optional[VectorStore] = None):
        """Initialize RAG tool with vector store."""
        super().__init__()
        self.vector_store = vector_store or VectorStore()
    
    def _run(self, query: str) -> str:
        """
        Search for relevant information in the document vector store.
        
        Args:
            query: The search query
            
        Returns:
            Relevant text chunks from the documents
        """
        try:
            # Check if vector store has documents
            doc_count = self.vector_store.get_collection_count()
            
            if doc_count == 0:
                return "No documents have been uploaded yet. Please upload course materials first."
            
            # Query vector store
            results = self.vector_store.query(query, n_results=5)
            
            # Format results with source information
            formatted_results = []
            for i, (doc, metadata, distance) in enumerate(
                zip(results["documents"], results["metadatas"], results["distances"]), 
                start=1
            ):
                page_info = f"Page {metadata.get('page_number', 'Unknown')}" if metadata.get('page_number') else "Unknown page"
                file_info = metadata.get('file_name', 'Unknown file')
                
                formatted_results.append(
                    f"[Result {i}] ({file_info}, {page_info}):\n{doc}\n"
                )
            
            result_text = "\n---\n".join(formatted_results)
            
            logger.info(f"RAG tool retrieved {len(results['documents'])} results for query: {query[:50]}...")
            
            return result_text
            
        except Exception as e:
            error_msg = f"Error retrieving documents: {str(e)}"
            logger.error(error_msg)
            return error_msg


def get_rag_tool(vector_store: Optional[VectorStore] = None) -> RAGTool:
    """
    Get configured RAG tool instance.
    
    Args:
        vector_store: Optional VectorStore instance
        
    Returns:
        RAGTool instance
    """
    return RAGTool(vector_store=vector_store)
