"""Text chunking and embedding utilities."""

from typing import List, Dict
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from loguru import logger
import sys
sys.path.append(str(__file__).rsplit('/', 3)[0])
from config.settings import OPENAI_API_KEY, EMBEDDING_MODEL, CHUNK_SIZE, CHUNK_OVERLAP


class EmbeddingManager:
    """Manage text chunking and embedding generation."""
    
    def __init__(self):
        """Initialize embedding manager with OpenAI embeddings."""
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=OPENAI_API_KEY,
            model=EMBEDDING_MODEL
        )
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        logger.info(f"Initialized EmbeddingManager with model: {EMBEDDING_MODEL}")
    
    def chunk_text(self, text: str, metadata: Dict = None) -> List[Dict]:
        """
        Split text into chunks with metadata.
        
        Args:
            text: Text to chunk
            metadata: Optional metadata to attach to each chunk
            
        Returns:
            List of dictionaries containing chunks and metadata
        """
        try:
            chunks = self.text_splitter.split_text(text)
            
            chunked_docs = []
            for i, chunk in enumerate(chunks):
                doc = {
                    "text": chunk,
                    "chunk_id": i,
                    "metadata": metadata or {}
                }
                chunked_docs.append(doc)
            
            logger.info(f"Split text into {len(chunks)} chunks")
            return chunked_docs
            
        except Exception as e:
            logger.error(f"Error chunking text: {str(e)}")
            raise
    
    def chunk_pages(self, pages: List[Dict], file_metadata: Dict = None) -> List[Dict]:
        """
        Chunk text from multiple pages with page tracking.
        
        Args:
            pages: List of page dictionaries with 'page_number' and 'text'
            file_metadata: File-level metadata
            
        Returns:
            List of chunked documents with page metadata
        """
        try:
            all_chunks = []
            
            for page in pages:
                page_text = page.get("text", "")
                page_num = page.get("page_number")
                
                chunks = self.text_splitter.split_text(page_text)
                
                for i, chunk in enumerate(chunks):
                    doc = {
                        "text": chunk,
                        "chunk_id": len(all_chunks),
                        "metadata": {
                            "page_number": page_num,
                            "chunk_within_page": i,
                            **(file_metadata or {})
                        }
                    }
                    all_chunks.append(doc)
            
            logger.info(f"Created {len(all_chunks)} chunks from {len(pages)} pages")
            return all_chunks
            
        except Exception as e:
            logger.error(f"Error chunking pages: {str(e)}")
            raise
    
    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.
        
        Args:
            texts: List of text strings
            
        Returns:
            List of embedding vectors
        """
        try:
            embeddings = self.embeddings.embed_documents(texts)
            logger.info(f"Generated embeddings for {len(texts)} texts")
            return embeddings
            
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise
    
    def get_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text string
            
        Returns:
            Embedding vector
        """
        try:
            embedding = self.embeddings.embed_query(text)
            return embedding
            
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            raise
