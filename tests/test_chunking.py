"""Tests for the chunking module."""

import pytest
from pdf2vector.core.chunking import MarkdownChunker, Chunk

@pytest.fixture
def chunker():
    """Create a MarkdownChunker instance for testing."""
    return MarkdownChunker(min_chunk_size=50, max_chunk_size=200)

def test_clean_text(chunker):
    """Test cleaning text."""
    text = """
    Page 1
    
    # Heading 1
    
    Some text with a URL: https://example.com
    
    ```python
    def hello():
        print("Hello, World!")
    ```
    
    ![Image](image.png)
    
    Page 2
    """
    
    cleaned = chunker.clean_text(text)
    
    # Check that boilerplate was removed
    assert "Page 1" not in cleaned
    assert "Page 2" not in cleaned
    assert "```python" not in cleaned
    assert "![Image]" not in cleaned
    assert "https://example.com" not in cleaned
    
    # Check that content was preserved
    assert "Heading 1" in cleaned
    assert "Some text" in cleaned

def test_split_by_headings(chunker):
    """Test splitting text by headings."""
    text = """
    # Heading 1
    
    Text under heading 1.
    
    ## Subheading
    
    More text.
    
    # Heading 2
    
    Text under heading 2.
    """
    
    chunks = chunker.split_by_headings(text)
    
    assert len(chunks) == 2
    assert "Heading 1" in chunks[0]
    assert "Text under heading 1" in chunks[0]
    assert "Heading 2" in chunks[1]
    assert "Text under heading 2" in chunks[1]

def test_split_by_paragraphs(chunker):
    """Test splitting text by paragraphs."""
    text = """
    First paragraph.
    
    Second paragraph.
    
    Third paragraph.
    """
    
    chunks = chunker.split_by_paragraphs(text)
    
    assert len(chunks) == 3
    assert "First paragraph" in chunks[0]
    assert "Second paragraph" in chunks[1]
    assert "Third paragraph" in chunks[2]

def test_merge_small_chunks(chunker):
    """Test merging small chunks."""
    chunks = [
        "Small chunk 1",
        "Small chunk 2",
        "This is a much longer chunk that should be kept separate",
        "Small chunk 3",
        "Small chunk 4"
    ]
    
    merged = chunker.merge_small_chunks(chunks)
    
    assert len(merged) == 3
    assert "Small chunk 1" in merged[0]
    assert "Small chunk 2" in merged[0]
    assert "This is a much longer chunk" in merged[1]
    assert "Small chunk 3" in merged[2]
    assert "Small chunk 4" in merged[2]

def test_chunk_text(chunker):
    """Test chunking text with metadata."""
    text = """
    # Heading 1
    
    Text under heading 1.
    
    ## Subheading
    
    More text.
    
    # Heading 2
    
    Text under heading 2.
    """
    
    metadata = {"filename": "test.md"}
    
    chunks = chunker.chunk_text(text, metadata)
    
    assert len(chunks) == 2
    assert isinstance(chunks[0], Chunk)
    assert chunks[0].text
    assert chunks[0].metadata["filename"] == "test.md"
    assert "chunk_index" in chunks[0].metadata
    assert "chunk_size" in chunks[0].metadata

def test_chunk_text_small(chunker):
    """Test chunking small text."""
    text = "This is a small piece of text."
    metadata = {"filename": "test.md"}
    
    chunks = chunker.chunk_text(text, metadata)
    
    assert len(chunks) == 1
    assert chunks[0].text == text
    assert chunks[0].metadata["filename"] == "test.md" 