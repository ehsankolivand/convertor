"""
Claude integration module for pdf2vector.

This module handles interacting with Claude's API for question answering.
"""

import logging
import os
from typing import List, Dict, Any, Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class ClaudeError(Exception):
    """Custom exception for Claude API errors."""
    pass

class ClaudeClient:
    """Client for interacting with Claude's API."""
    
    def __init__(self, api_key: str = None):
        """
        Initialize the Claude client.
        
        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("Anthropic API key not found. Set ANTHROPIC_API_KEY environment variable.")
            
        # Configure retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        
        # Create session with retry strategy
        self.session = requests.Session()
        self.session.mount("https://", HTTPAdapter(max_retries=retry_strategy))
        
    def _format_context(self, chunks: List[Dict[str, Any]]) -> str:
        """
        Format retrieved chunks as context for Claude.
        
        Args:
            chunks: List of retrieved chunks with text and metadata
            
        Returns:
            str: Formatted context string
        """
        context_parts = []
        for chunk in chunks:
            context_parts.append(
                f"Source: {chunk['metadata'].get('filename', 'unknown')} "
                f"(Chunk {chunk['metadata'].get('chunk_index', '?')})\n"
                f"{chunk['text']}\n"
            )
        return "\n".join(context_parts)
        
    def answer_question(
        self,
        question: str,
        context_chunks: List[Dict[str, Any]],
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Answer a question using Claude with retrieved context.
        
        Args:
            question: The question to answer
            context_chunks: List of retrieved context chunks
            conversation_history: Optional conversation history
            
        Returns:
            Dict[str, Any]: Response with answer and sources
            
        Raises:
            ClaudeError: If there's an error getting the answer
        """
        try:
            # Format context
            context = self._format_context(context_chunks)
            
            # Build messages
            messages = []
            
            # Add system message
            messages.append({
                "role": "system",
                "content": (
                    "You are a helpful AI assistant that answers questions based on the provided context. "
                    "Always cite your sources using the chunk information provided. "
                    "If you cannot answer the question based on the context, say so."
                )
            })
            
            # Add conversation history
            if conversation_history:
                messages.extend(conversation_history)
                
            # Add context and question
            messages.append({
                "role": "user",
                "content": (
                    f"Context:\n{context}\n\n"
                    f"Question: {question}\n\n"
                    "Please answer the question based on the context above. "
                    "Include source citations in your answer."
                )
            })
            
            # Call Claude API
            response = self.session.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json"
                },
                json={
                    "model": "claude-3-opus-20240229",
                    "max_tokens": 1000,
                    "messages": messages
                }
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Extract sources from context chunks
            sources = [
                {
                    "filename": chunk["metadata"].get("filename", "unknown"),
                    "chunk_index": chunk["metadata"].get("chunk_index", "?")
                }
                for chunk in context_chunks
            ]
            
            return {
                "answer": result["content"][0]["text"],
                "sources": sources
            }
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Error getting answer from Claude: {str(e)}"
            logger.error(error_msg)
            raise ClaudeError(error_msg)
            
    def __del__(self):
        """Clean up resources."""
        if hasattr(self, 'session'):
            self.session.close() 