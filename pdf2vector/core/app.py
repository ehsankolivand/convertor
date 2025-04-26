"""
Core application module for pdf2vector.

This module provides the main PDF2Vector class that coordinates
PDF processing, vector storage, and question answering.
"""

import logging
from pathlib import Path
from typing import Dict, List, Any

from .chunking import PDFChunker
from .embeddings import EmbeddingGenerator
from .vector_store import ChromaDBStore

logger = logging.getLogger(__name__)

class PDF2Vector:
    """Main application class for PDF to vector conversion."""
    
    def __init__(self, input_dir: str, persist_dir: str):
        """Initialize the application.
        
        Args:
            input_dir: Directory to watch for PDF files.
            persist_dir: Directory to persist the vector store.
        """
        self.input_dir = Path(input_dir)
        self.persist_dir = Path(persist_dir)
        
        # Initialize components
        self.chunker = PDFChunker()
        self.embedding_generator = EmbeddingGenerator()
        self.vector_store = ChromaDBStore(
            persist_dir=self.persist_dir,
            embedding_generator=self.embedding_generator
        )
        
        logger.info("Initialized PDF2Vector application")
        
    def process_pdf(self, pdf_path: Path):
        """Process a PDF file.
        
        Args:
            pdf_path: Path to the PDF file.
        """
        try:
            logger.info(f"Processing PDF: {pdf_path}")
            
            # Extract text and chunk
            chunks = self.chunker.chunk_pdf(pdf_path)
            
            # Store chunks in vector store
            self.vector_store.upsert(chunks)
            
            logger.info(f"Successfully processed PDF: {pdf_path}")
            
        except Exception as e:
            logger.error(f"Error processing PDF {pdf_path}: {str(e)}")
            raise
            
    def ask_question(self, question: str) -> Dict[str, Any]:
        """Answer a question using the vector store.
        
        Args:
            question: Question to answer.
            
        Returns:
            Dictionary containing answer and sources.
        """
        try:
            # Query vector store
            chunks = self.vector_store.query(question)
            
            # Format response
            response = {
                "answer": "Here are the relevant passages from the documents:",
                "sources": []
            }
            
            # Add chunks to response
            for chunk in chunks:
                response["sources"].append({
                    "text": chunk["text"],
                    "filename": chunk["metadata"]["filename"],
                    "chunk_index": chunk["metadata"]["chunk_index"]
                })
                
            return response
            
        except Exception as e:
            logger.error(f"Error answering question: {str(e)}")
            raise 