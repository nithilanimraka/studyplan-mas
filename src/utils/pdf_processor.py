"""PDF processing utilities."""

from pathlib import Path
from typing import List, Dict
from pypdf import PdfReader
from loguru import logger


class PDFProcessor:
    """Handle PDF text extraction with page tracking."""
    
    def __init__(self):
        """Initialize PDF processor."""
        pass
    
    def extract_text_from_pdf(self, file_path: str) -> Dict[str, any]:
        """
        Extract text from a PDF file with page information.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Dictionary containing full text, pages, and metadata
        """
        try:
            reader = PdfReader(file_path)
            
            pages = []
            full_text = ""
            
            for page_num, page in enumerate(reader.pages, start=1):
                page_text = page.extract_text()
                if page_text:
                    pages.append({
                        "page_number": page_num,
                        "text": page_text
                    })
                    full_text += f"\n\n--- Page {page_num} ---\n\n{page_text}"
            
            metadata = {
                "total_pages": len(reader.pages),
                "file_name": Path(file_path).name
            }
            
            logger.info(f"Successfully extracted text from {metadata['file_name']} ({metadata['total_pages']} pages)")
            
            return {
                "full_text": full_text.strip(),
                "pages": pages,
                "metadata": metadata
            }
            
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            raise
    
    def extract_text_from_bytes(self, file_bytes: bytes, file_name: str) -> Dict[str, any]:
        """
        Extract text from PDF bytes (useful for uploaded files).
        
        Args:
            file_bytes: PDF file content as bytes
            file_name: Name of the file
            
        Returns:
            Dictionary containing full text, pages, and metadata
        """
        try:
            from io import BytesIO
            
            pdf_file = BytesIO(file_bytes)
            reader = PdfReader(pdf_file)
            
            pages = []
            full_text = ""
            
            for page_num, page in enumerate(reader.pages, start=1):
                page_text = page.extract_text()
                if page_text:
                    pages.append({
                        "page_number": page_num,
                        "text": page_text
                    })
                    full_text += f"\n\n--- Page {page_num} ---\n\n{page_text}"
            
            metadata = {
                "total_pages": len(reader.pages),
                "file_name": file_name
            }
            
            logger.info(f"Successfully extracted text from {file_name} ({metadata['total_pages']} pages)")
            
            return {
                "full_text": full_text.strip(),
                "pages": pages,
                "metadata": metadata
            }
            
        except Exception as e:
            logger.error(f"Error extracting text from PDF bytes: {str(e)}")
            raise
