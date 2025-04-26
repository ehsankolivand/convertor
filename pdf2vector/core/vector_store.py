"""
Vector store module for pdf2vector.

This module provides functionality to store and retrieve vector embeddings
using ChromaDB.
"""

import logging
import hashlib
from pathlib import Path
from typing import List, Dict, Any

import chromadb
from chromadb.config import Settings

from .chunking import Chunk
from .embeddings import EmbeddingGenerator

logger = logging.getLogger(__name__)

class ChromaDBStore:
    """Manages vector storage and retrieval using ChromaDB."""
    
    def __init__(self, persist_dir: Path, embedding_generator: EmbeddingGenerator):
        """Initialize the vector store.
        
        Args:
            persist_dir: Directory to persist the ChromaDB database.
            embedding_generator: Generator for creating embeddings.
        """
        self.persist_dir = Path(persist_dir)
        self.embedding_generator = embedding_generator
        
        # Create persist directory if it doesn't exist
        if not self.persist_dir.exists():
            self.persist_dir.mkdir(parents=True)
            
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=str(self.persist_dir),
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="pdf_learning",
            metadata={"hnsw:space": "cosine"}
        )
        
        logger.info(f"Initialized ChromaDB store at {self.persist_dir}")
        
    def _generate_id(self, chunk: Chunk) -> str:
        """Generate a unique ID for a chunk.
        
        Args:
            chunk: Chunk object containing text and metadata.
            
        Returns:
            str: Unique ID for the chunk.
        """
        # Create a unique string from chunk content
        content = f"{chunk.text}{chunk.metadata['filename']}{chunk.metadata['chunk_index']}"
        return hashlib.sha256(content.encode()).hexdigest()
        
    def upsert(self, chunks: List[Chunk]):
        """Store chunks in the vector store.
        
        Args:
            chunks: List of Chunk objects to store.
        """
        try:
            # Prepare data for bulk upsert
            ids = []
            texts = []
            metadatas = []
            embeddings = []
            
            for chunk in chunks:
                # Generate embedding
                embedding = self.embedding_generator.embed_text(chunk.text)
                
                # Prepare data
                ids.append(self._generate_id(chunk))
                texts.append(chunk.text)
                metadatas.append(chunk.metadata)
                embeddings.append(embedding)
                
            # Perform bulk upsert
            self.collection.upsert(
                ids=ids,
                documents=texts,
                metadatas=metadatas,
                embeddings=embeddings
            )
            
            logger.info(f"Successfully stored {len(chunks)} chunks")
            
        except Exception as e:
            logger.error(f"Error storing chunks: {str(e)}")
            raise
            
    def query(self, question: str, k: int = 5) -> List[Dict[str, Any]]:
        """Query the vector store for similar chunks.
        
        Args:
            question: Question to search for.
            k: Number of results to return.
            
        Returns:
            List of dictionaries containing text and metadata for matching chunks.
        """
        try:
            # Generate embedding for question
            question_embedding = self.embedding_generator.embed_text(question)
            
            # Query collection
            results = self.collection.query(
                query_embeddings=[question_embedding],
                n_results=k
            )
            
            # Format results
            chunks = []
            for i in range(len(results['documents'][0])):
                chunk = {
                    'text': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i]
                }
                chunks.append(chunk)
                
            return chunks
            
        except Exception as e:
            logger.error(f"Error querying vector store: {str(e)}")
            raise 