import pytest
from pathlib import Path
from src.converter import convert_pdf_to_markdown, ConversionError

def test_file_not_found():
    with pytest.raises(ConversionError) as exc_info:
        convert_pdf_to_markdown("nonexistent.pdf")
    assert "File not found" in str(exc_info.value)

def test_empty_conversion(tmp_path):
    # Create an empty PDF file
    pdf_path = tmp_path / "empty.pdf"
    pdf_path.write_bytes(b"")
    
    with pytest.raises(ConversionError) as exc_info:
        convert_pdf_to_markdown(str(pdf_path))
    assert "no text content was extracted" in str(exc_info.value)

def test_invalid_pdf(tmp_path):
    # Create an invalid PDF file
    pdf_path = tmp_path / "invalid.pdf"
    pdf_path.write_text("This is not a PDF file")
    
    with pytest.raises(ConversionError):
        convert_pdf_to_markdown(str(pdf_path))

@pytest.mark.skip(reason="Requires a valid PDF file for testing")
def test_successful_conversion():
    # This test requires a valid PDF file
    # You would need to add a test PDF file to the tests/data directory
    pdf_path = Path("tests/data/sample.pdf")
    result = convert_pdf_to_markdown(str(pdf_path))
    assert result
    assert not result.startswith("# Error:") 