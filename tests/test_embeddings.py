"""Tests for the embeddings module."""

import pytest
from unittest.mock import Mock, patch
import requests

from pdf2vector.core.embeddings import EmbeddingGenerator, EmbeddingError

@pytest.fixture
def mock_session():
    """Create a mock requests session."""
    with patch("requests.Session") as mock:
        session = Mock()
        mock.return_value = session
        yield session

@pytest.fixture
def generator(mock_session):
    """Create an EmbeddingGenerator instance with a mock session."""
    with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
        return EmbeddingGenerator()

def test_init_with_env_var():
    """Test initialization with environment variable."""
    with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
        generator = EmbeddingGenerator()
        assert generator.api_key == "test-key"

def test_init_with_api_key():
    """Test initialization with API key."""
    generator = EmbeddingGenerator(api_key="test-key")
    assert generator.api_key == "test-key"

def test_init_without_api_key():
    """Test initialization without API key."""
    with patch.dict("os.environ", {}, clear=True):
        with pytest.raises(ValueError, match="OpenAI API key not found"):
            EmbeddingGenerator()

def test_generate_embedding_success(generator, mock_session):
    """Test successful embedding generation."""
    # Mock response
    mock_response = Mock()
    mock_response.json.return_value = {
        "data": [{"embedding": [0.1, 0.2, 0.3]}]
    }
    mock_session.post.return_value = mock_response
    
    # Generate embedding
    embedding = generator.generate_embedding("Test text")
    
    # Check API call
    mock_session.post.assert_called_once_with(
        "https://api.openai.com/v1/embeddings",
        headers={
            "Authorization": "Bearer test-key",
            "Content-Type": "application/json"
        },
        json={
            "model": "text-embedding-3-small",
            "input": "Test text"
        }
    )
    
    # Check result
    assert embedding == [0.1, 0.2, 0.3]

def test_generate_embedding_error(generator, mock_session):
    """Test embedding generation error."""
    # Mock error response
    mock_session.post.side_effect = requests.exceptions.RequestException("API Error")
    
    # Test error handling
    with pytest.raises(EmbeddingError, match="Error generating embedding"):
        generator.generate_embedding("Test text")

def test_generate_embeddings_success(generator, mock_session):
    """Test successful batch embedding generation."""
    # Mock response
    mock_response = Mock()
    mock_response.json.return_value = {
        "data": [
            {"embedding": [0.1, 0.2, 0.3]},
            {"embedding": [0.4, 0.5, 0.6]}
        ]
    }
    mock_session.post.return_value = mock_response
    
    # Generate embeddings
    texts = ["Text 1", "Text 2"]
    embeddings = generator.generate_embeddings(texts)
    
    # Check API call
    mock_session.post.assert_called_once_with(
        "https://api.openai.com/v1/embeddings",
        headers={
            "Authorization": "Bearer test-key",
            "Content-Type": "application/json"
        },
        json={
            "model": "text-embedding-3-small",
            "input": texts
        }
    )
    
    # Check result
    assert len(embeddings) == 2
    assert embeddings[0] == [0.1, 0.2, 0.3]
    assert embeddings[1] == [0.4, 0.5, 0.6]

def test_generate_embeddings_error(generator, mock_session):
    """Test batch embedding generation error."""
    # Mock error response
    mock_session.post.side_effect = requests.exceptions.RequestException("API Error")
    
    # Test error handling
    with pytest.raises(EmbeddingError, match="Error generating embeddings"):
        generator.generate_embeddings(["Text 1", "Text 2"])

def test_cleanup(generator, mock_session):
    """Test cleanup of resources."""
    del generator
    mock_session.close.assert_called_once() 