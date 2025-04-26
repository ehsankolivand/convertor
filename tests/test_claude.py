"""Tests for the Claude integration module."""

import pytest
from unittest.mock import Mock, patch
import requests

from pdf2vector.core.claude import ClaudeClient, ClaudeError

@pytest.fixture
def mock_session():
    """Create a mock requests session."""
    with patch("requests.Session") as mock:
        session = Mock()
        mock.return_value = session
        yield session

@pytest.fixture
def client(mock_session):
    """Create a ClaudeClient instance with a mock session."""
    with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"}):
        return ClaudeClient()

def test_init_with_env_var():
    """Test initialization with environment variable."""
    with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"}):
        client = ClaudeClient()
        assert client.api_key == "test-key"

def test_init_with_api_key():
    """Test initialization with API key."""
    client = ClaudeClient(api_key="test-key")
    assert client.api_key == "test-key"

def test_init_without_api_key():
    """Test initialization without API key."""
    with patch.dict("os.environ", {}, clear=True):
        with pytest.raises(ValueError, match="Anthropic API key not found"):
            ClaudeClient()

def test_format_context(client):
    """Test formatting context from chunks."""
    chunks = [
        {
            "text": "Text 1",
            "metadata": {"filename": "doc1.pdf", "chunk_index": 0}
        },
        {
            "text": "Text 2",
            "metadata": {"filename": "doc1.pdf", "chunk_index": 1}
        }
    ]
    
    context = client._format_context(chunks)
    
    assert "Source: doc1.pdf (Chunk 0)" in context
    assert "Text 1" in context
    assert "Source: doc1.pdf (Chunk 1)" in context
    assert "Text 2" in context

def test_answer_question_success(client, mock_session):
    """Test successful question answering."""
    # Mock response
    mock_response = Mock()
    mock_response.json.return_value = {
        "content": [{"text": "Test answer"}]
    }
    mock_session.post.return_value = mock_response
    
    # Test data
    question = "Test question?"
    chunks = [
        {
            "text": "Text 1",
            "metadata": {"filename": "doc1.pdf", "chunk_index": 0}
        }
    ]
    
    response = client.answer_question(question, chunks)
    
    # Check API call
    mock_session.post.assert_called_once()
    call_args = mock_session.post.call_args
    
    assert call_args[0][0] == "https://api.anthropic.com/v1/messages"
    assert call_args[1]["headers"]["x-api-key"] == "test-key"
    assert call_args[1]["json"]["model"] == "claude-3-opus-20240229"
    assert "Test question?" in call_args[1]["json"]["messages"][-1]["content"]
    
    # Check response
    assert response["answer"] == "Test answer"
    assert len(response["sources"]) == 1
    assert response["sources"][0]["filename"] == "doc1.pdf"
    assert response["sources"][0]["chunk_index"] == 0

def test_answer_question_with_history(client, mock_session):
    """Test question answering with conversation history."""
    # Mock response
    mock_response = Mock()
    mock_response.json.return_value = {
        "content": [{"text": "Test answer"}]
    }
    mock_session.post.return_value = mock_response
    
    # Test data
    question = "Test question?"
    chunks = [
        {
            "text": "Text 1",
            "metadata": {"filename": "doc1.pdf", "chunk_index": 0}
        }
    ]
    history = [
        {"role": "user", "content": "Previous question"},
        {"role": "assistant", "content": "Previous answer"}
    ]
    
    response = client.answer_question(question, chunks, history)
    
    # Check that history was included
    call_args = mock_session.post.call_args
    messages = call_args[1]["json"]["messages"]
    assert len(messages) == 4  # system + 2 history + current
    assert messages[1]["content"] == "Previous question"
    assert messages[2]["content"] == "Previous answer"

def test_answer_question_error(client, mock_session):
    """Test question answering error."""
    # Mock error response
    mock_session.post.side_effect = requests.exceptions.RequestException("API Error")
    
    # Test error handling
    with pytest.raises(ClaudeError, match="Error getting answer from Claude"):
        client.answer_question("Test question?", [])

def test_cleanup(client, mock_session):
    """Test cleanup of resources."""
    del client
    mock_session.close.assert_called_once() 