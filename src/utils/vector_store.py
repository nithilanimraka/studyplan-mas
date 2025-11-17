"""Vector store management with ChromaDB."""

from typing import List, Dict, Optional
import chromadb
from chromadb.config import Settings
from loguru import logger
import sys
sys.path.append(str(__file__).rsplit('/', 3)[0])
from config.settings import CHROMA_PERSIST_DIR
from src.utils.embeddings import EmbeddingManager


class VectorStore:
    """Manage ChromaDB vector store for document retrieval."""
    
    def __init__(self, collection_name: str = "assignment_documents"):
        """
        Initialize ChromaDB vector store.
        
        Args:
            collection_name: Name of the collection to use
        """
        self.collection_name = collection_name
        self.embedding_manager = EmbeddingManager()
        
        # Initialize ChromaDB client with persistence
        self.client = chromadb.PersistentClient(
            path=CHROMA_PERSIST_DIR,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        
        logger.info(f"Initialized VectorStore with collection: {collection_name}")
    
    def add_documents(self, chunks: List[Dict]) -> None:
        """
        Add document chunks to the vector store.
        
        Args:
            chunks: List of chunk dictionaries with 'text' and 'metadata'
        """
        try:
            texts = [chunk["text"] for chunk in chunks]
            metadatas = [chunk["metadata"] for chunk in chunks]
            ids = [f"chunk_{chunk['chunk_id']}" for chunk in chunks]
            
            # Generate embeddings
            embeddings = self.embedding_manager.get_embeddings(texts)
            
            # Add to ChromaDB
            self.collection.add(
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"Added {len(chunks)} documents to vector store")
            
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {str(e)}")
            raise
    
    def query(self, query_text: str, n_results: int = 5) -> Dict:
        """
        Query the vector store for similar documents.
        
        Args:
            query_text: Query string
            n_results: Number of results to return
            
        Returns:
            Dictionary with documents, metadatas, and distances
        """
        try:
            # Generate query embedding
            query_embedding = self.embedding_manager.get_embedding(query_text)
            
            # Query ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                include=["documents", "metadatas", "distances"]
            )
            
            logger.info(f"Retrieved {len(results['documents'][0])} results for query")
            
            return {
                "documents": results["documents"][0],
                "metadatas": results["metadatas"][0],
                "distances": results["distances"][0]
            }
            
        except Exception as e:
            logger.error(f"Error querying vector store: {str(e)}")
            raise
    
    def clear_collection(self) -> None:
        """Clear all documents from the collection."""
        try:
            # Delete and recreate collection
            self.client.delete_collection(name=self.collection_name)
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            logger.info(f"Cleared collection: {self.collection_name}")
            
        except Exception as e:
            logger.error(f"Error clearing collection: {str(e)}")
            raise
    
    def get_collection_count(self) -> int:
        """Get the number of documents in the collection."""
        try:
            count = self.collection.count()
            return count
        except Exception as e:
            logger.error(f"Error getting collection count: {str(e)}")
            return 0
    
    def delete_collection(self) -> None:
        """Delete the entire collection."""
        try:
            self.client.delete_collection(name=self.collection_name)
            logger.info(f"Deleted collection: {self.collection_name}")
        except Exception as e:
            logger.error(f"Error deleting collection: {str(e)}")
            raise
