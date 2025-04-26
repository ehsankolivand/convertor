"""
Embeddings module for pdf2vector.

This module handles generating embeddings using OpenAI's API with retry logic.
"""

import logging
import os
from typing import List, Dict, Any
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class EmbeddingError(Exception):
    """Custom exception for embedding generation errors."""
    pass

class EmbeddingGenerator:
    """Generates embeddings using OpenAI's API."""
    
    def __init__(self, api_key: str = None):
        """
        Initialize the embedding generator.
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
            
        # Configure retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        
        # Create session with retry strategy
        self.session = requests.Session()
        self.session.mount("https://", HTTPAdapter(max_retries=retry_strategy))
        
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text to generate embedding for
            
        Returns:
            List[float]: The generated embedding vector
            
        Raises:
            EmbeddingError: If there's an error generating the embedding
        """
        try:
            response = self.session.post(
                "https://api.openai.com/v1/embeddings",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "text-embedding-3-small",
                    "input": text
                }
            )
            
            response.raise_for_status()
            return response.json()["data"][0]["embedding"]
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Error generating embedding: {str(e)}"
            logger.error(error_msg)
            raise EmbeddingError(error_msg)
            
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts: List of texts to generate embeddings for
            
        Returns:
            List[List[float]]: List of embedding vectors
            
        Raises:
            EmbeddingError: If there's an error generating the embeddings
        """
        try:
            response = self.session.post(
                "https://api.openai.com/v1/embeddings",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "text-embedding-3-small",
                    "input": texts
                }
            )
            
            response.raise_for_status()
            return [item["embedding"] for item in response.json()["data"]]
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Error generating embeddings: {str(e)}"
            logger.error(error_msg)
            raise EmbeddingError(error_msg)
            
    def __del__(self):
        """Clean up resources."""
        if hasattr(self, 'session'):
            self.session.close() 