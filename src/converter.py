import logging
from pathlib import Path
from typing import Optional

from markitdown import MarkItDown

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ConversionError(Exception):
    """Custom exception for PDF conversion errors."""
    pass

def convert_pdf_to_markdown(pdf_file_path: str, enable_plugins: bool = False) -> str:
    """
    Converts a PDF file to Markdown text using the markitdown library.

    Args:
        pdf_file_path (str): Path to the PDF file to convert
        enable_plugins (bool): Whether to enable markitdown plugins (default: False)

    Returns:
        str: The converted Markdown text

    Raises:
        ConversionError: If there's an error during conversion
    """
    pdf_path = Path(pdf_file_path)
    
    if not pdf_path.exists():
        error_msg = f"File not found: {pdf_file_path}"
        logger.error(error_msg)
        raise ConversionError(error_msg)

    try:
        logger.info(f"Starting conversion of {pdf_path}")
        md_converter = MarkItDown(enable_plugins=enable_plugins)

        with open(pdf_path, 'rb') as f:
            result = md_converter.convert_stream(f)
            
            if not result:
                error_msg = "Conversion returned no result"
                logger.error(error_msg)
                raise ConversionError(error_msg)
                
            if not hasattr(result, 'text_content'):
                error_msg = "Conversion result missing text_content attribute"
                logger.error(error_msg)
                raise ConversionError(error_msg)
                
            if not result.text_content:
                error_msg = "Conversion completed but no text content was extracted"
                logger.warning(error_msg)
                raise ConversionError(error_msg)
                
            logger.info(f"Successfully converted {pdf_path}")
            return result.text_content

    except ImportError as e:
        error_msg = f"Required library not found: {str(e)}"
        logger.error(error_msg)
        raise ConversionError(error_msg)
    except Exception as e:
        error_msg = f"Unexpected error during conversion: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise ConversionError(error_msg) 