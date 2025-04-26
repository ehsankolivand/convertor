"""
Chunking module for pdf2vector.

This module handles splitting markdown text into semantically coherent chunks.
"""

import re
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class Chunk:
    """Represents a chunk of text with metadata."""
    text: str
    metadata: Dict[str, Any]
    
class MarkdownChunker:
    """Splits markdown text into semantically coherent chunks."""
    
    def __init__(self, min_chunk_size: int = 100, max_chunk_size: int = 1000):
        """
        Initialize the markdown chunker.
        
        Args:
            min_chunk_size: Minimum size of a chunk in characters
            max_chunk_size: Maximum size of a chunk in characters
        """
        self.min_chunk_size = min_chunk_size
        self.max_chunk_size = max_chunk_size
        
    def clean_text(self, text: str) -> str:
        """
        Clean the text by removing boilerplate and non-text artifacts.
        
        Args:
            text: The text to clean
            
        Returns:
            str: The cleaned text
        """
        # Remove page numbers
        text = re.sub(r'\n\s*\d+\s*\n', '\n', text)
        
        # Remove code fences
        text = re.sub(r'```[\s\S]*?```', '', text)
        
        # Remove image references
        text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
        
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text
        
    def split_by_headings(self, text: str) -> List[str]:
        """
        Split text by headings.
        
        Args:
            text: The text to split
            
        Returns:
            List[str]: List of text chunks
        """
        # Split by heading markers (#)
        chunks = re.split(r'(?=^#+\s)', text, flags=re.MULTILINE)
        return [chunk.strip() for chunk in chunks if chunk.strip()]
        
    def split_by_paragraphs(self, text: str) -> List[str]:
        """
        Split text by paragraphs.
        
        Args:
            text: The text to split
            
        Returns:
            List[str]: List of text chunks
        """
        # Split by blank lines
        chunks = re.split(r'\n\s*\n', text)
        return [chunk.strip() for chunk in chunks if chunk.strip()]
        
    def merge_small_chunks(self, chunks: List[str]) -> List[str]:
        """
        Merge small chunks to meet minimum size requirement.
        
        Args:
            chunks: List of text chunks
            
        Returns:
            List[str]: List of merged chunks
        """
        merged = []
        current_chunk = ""
        
        for chunk in chunks:
            if len(current_chunk) + len(chunk) <= self.max_chunk_size:
                current_chunk += "\n\n" + chunk if current_chunk else chunk
            else:
                if current_chunk:
                    merged.append(current_chunk)
                current_chunk = chunk
                
        if current_chunk:
            merged.append(current_chunk)
            
        return merged
        
    def chunk_text(self, text: str, metadata: Dict[str, Any]) -> List[Chunk]:
        """
        Split text into semantically coherent chunks.
        
        Args:
            text: The text to chunk
            metadata: Metadata to attach to each chunk
            
        Returns:
            List[Chunk]: List of chunks with metadata
        """
        # Clean the text
        text = self.clean_text(text)
        
        # First try splitting by headings
        chunks = self.split_by_headings(text)
        
        # If chunks are too small, split by paragraphs
        if any(len(chunk) < self.min_chunk_size for chunk in chunks):
            chunks = self.split_by_paragraphs(text)
            
        # Merge small chunks
        chunks = self.merge_small_chunks(chunks)
        
        # Create Chunk objects with metadata
        return [
            Chunk(
                text=chunk,
                metadata={
                    **metadata,
                    "chunk_index": i,
                    "chunk_size": len(chunk)
                }
            )
            for i, chunk in enumerate(chunks)
        ] 