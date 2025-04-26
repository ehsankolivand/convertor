"""
Module for generating vector embeddings from text using a simple hash-based approach.
"""

import logging
import hashlib
import numpy as np
from typing import List, Union

logger = logging.getLogger(__name__)

class EmbeddingGenerator:
    """Generates embeddings for text using a simple hash-based method."""
    
    def __init__(self, model_name: str = "simple-hash"):
        """Initialize the embedding generator.
        
        Args:
            model_name: Name of the embedding model (default: simple-hash)
        """
        self.model_name = model_name
        self.dimension = 1536  # Same dimension as text-embedding-ada-002 for compatibility
        
    def embed_text(self, text: Union[str, List[str]]) -> Union[List[float], List[List[float]]]:
        """Generate embeddings for the given text.
        
        Args:
            text: Single string or list of strings to embed
            
        Returns:
            List of embeddings as floats, or list of lists for multiple texts
        """
        try:
            if isinstance(text, str):
                return self._generate_single_embedding(text)
            elif isinstance(text, list):
                return [self._generate_single_embedding(t) for t in text]
            else:
                raise ValueError(f"Unsupported input type: {type(text)}")
                
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise
            
    def _generate_single_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text string using hash-based approach.
        
        Args:
            text: Text string to embed
            
        Returns:
            List of floats representing the embedding
        """
        # Initialize embedding vector
        embedding = np.zeros(self.dimension)
        
        # Split text into words and hash each one
        words = text.split()
        for i, word in enumerate(words):
            # Get hash of word
            word_hash = int(hashlib.sha256(word.encode()).hexdigest(), 16)
            
            # Use hash to set values in embedding vector
            for j in range(min(32, self.dimension)):  # Use first 32 bytes of hash
                idx = (word_hash + j) % self.dimension
                val = ((word_hash >> j) & 0xFF) / 255.0  # Normalize to [0,1]
                embedding[idx] = val
                
        # Normalize the embedding vector
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
            
        return embedding.tolist()