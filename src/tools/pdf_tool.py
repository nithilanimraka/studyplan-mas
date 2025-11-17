"""PDF processing tool for CrewAI."""

from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from loguru import logger
import sys
sys.path.append(str(__file__).rsplit('/', 3)[0])
from src.utils.pdf_processor import PDFProcessor


class PDFExtractorInput(BaseModel):
    """Input schema for PDFExtractorTool."""
    file_path: str = Field(..., description="Path to the PDF file to extract text from")


class PDFExtractorTool(BaseTool):
    """Tool for extracting text from PDF files."""
    
    name: str = "PDF Text Extractor"
    description: str = (
        "Extracts text content from PDF files. "
        "Useful for reading and analyzing PDF documents, assignments, or study materials. "
        "Provide the file path as input."
    )
    args_schema: Type[BaseModel] = PDFExtractorInput
    
    def _run(self, file_path: str) -> str:
        """
        Extract text from a PDF file.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Extracted text content
        """
        try:
            processor = PDFProcessor()
            result = processor.extract_text_from_pdf(file_path)
            
            logger.info(f"PDF tool extracted text from {result['metadata']['file_name']}")
            
            return result['full_text']
            
        except Exception as e:
            error_msg = f"Error extracting text from PDF: {str(e)}"
            logger.error(error_msg)
            return error_msg


# Create tool instance
pdf_tool = PDFExtractorTool()
