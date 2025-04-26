"""
PDF chunking module for pdf2vector.

This module provides functionality to extract text from PDFs
and split it into chunks for processing.
"""

import logging
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass

from pdfminer.high_level import extract_text

logger = logging.getLogger(__name__)

@dataclass
class Chunk:
    """A chunk of text with metadata."""
    text: str
    metadata: Dict[str, Any]

class PDFChunker:
    """Extracts and chunks text from PDFs."""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """Initialize the chunker.
        
        Args:
            chunk_size: Target size of each chunk in characters.
            chunk_overlap: Number of characters to overlap between chunks.
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
    def chunk_pdf(self, pdf_path: Path) -> List[Chunk]:
        """Extract text from a PDF and split it into chunks.
        
        Args:
            pdf_path: Path to the PDF file.
            
        Returns:
            List of Chunk objects containing text and metadata.
        """
        try:
            # Extract text from PDF
            text = extract_text(str(pdf_path))
            
            # Split into chunks
            chunks = []
            start = 0
            chunk_index = 0
            
            while start < len(text):
                # Get chunk text
                end = start + self.chunk_size
                chunk_text = text[start:end]
                
                # Create chunk with metadata
                chunk = Chunk(
                    text=chunk_text,
                    metadata={
                        "filename": pdf_path.name,
                        "chunk_index": chunk_index
                    }
                )
                chunks.append(chunk)
                
                # Move to next chunk with overlap
                start = end - self.chunk_overlap
                chunk_index += 1
                
            logger.info(f"Split PDF into {len(chunks)} chunks")
            return chunks
            
        except Exception as e:
            logger.error(f"Error chunking PDF {pdf_path}: {str(e)}")
            raise 