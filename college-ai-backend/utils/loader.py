"""
Document loader utilities for PDF, DOCX, and TXT files.

Uses PyPDF2 and python-docx when available, but falls back to simple
text decoding if those packages aren't installed (for mock mode).

Cleans extracted text to remove metadata, page numbers, and irrelevant content.
"""
from typing import Optional
from io import BytesIO
import logging
import re

logger = logging.getLogger(__name__)


def clean_text(text: str) -> str:
    """
    Clean extracted text by removing metadata, page numbers, and formatting artifacts.
    """
    if not text:
        return ""
    
    lines = text.split('\n')
    cleaned_lines = []
    
    # Patterns to skip
    skip_patterns = [
        r'^\s*page\s+\d+',  # Page numbers
        r'^\s*\d+\s*$',  # Standalone numbers
        r'copyright\s+©',  # Copyright lines
        r'isbn[:\s]*[\d\-]+',  # ISBN numbers
        r'blind\s+folio',  # Publishing metadata
        r'compref',  # Reference codes
        r'^\s*\d{2}[-/]\d{2}[-/]\d{2,4}',  # Dates at line start
        r'^\s*chapter\s+\d+\s*$',  # Standalone chapter markers
        r'^\s*section\s+\d+\s*$',  # Standalone section markers
    ]
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue
        
        # Skip lines matching patterns
        if any(re.search(pattern, line, re.IGNORECASE) for pattern in skip_patterns):
            continue
        
        # Skip lines that are too short (likely artifacts)
        if len(line) < 3:
            continue
        
        cleaned_lines.append(line)
    
    # Join with spaces and normalize whitespace
    cleaned = ' '.join(cleaned_lines)
    cleaned = re.sub(r'\s+', ' ', cleaned)
    
    return cleaned.strip()


def process_file(filename: str, file_content: bytes) -> str:
    """
    Extract text content from uploaded file and clean it.
    
    Args:
        filename: Name of the file
        file_content: Raw bytes of the file
        
    Returns:
        Cleaned extracted text content
    """
    text = ""
    filename_lower = filename.lower()
    
    try:
        if filename_lower.endswith(".pdf"):
            text = _process_pdf(file_content)
        elif filename_lower.endswith(".docx"):
            text = _process_docx(file_content)
        elif filename_lower.endswith((".txt", ".md")):
            text = file_content.decode("utf-8", errors="ignore")
        else:
            # Try to decode as plain text
            text = file_content.decode("utf-8", errors="ignore")
            
    except Exception as e:
        logger.error(f"Error processing file {filename}: {e}")
        # Last resort fallback
        try:
            text = file_content.decode("utf-8", errors="ignore")
        except:
            text = ""
    
    # Clean the extracted text
    return clean_text(text)


def _process_pdf(file_content: bytes) -> str:
    """Extract text from PDF file."""
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(BytesIO(file_content))
        text_parts = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
        return "\n".join(text_parts)
    except ImportError:
        logger.warning("PyPDF2 not installed. Install it for PDF support: pip install PyPDF2")
        return "[PDF content - PyPDF2 not installed]"
    except Exception as e:
        logger.error(f"Error extracting PDF: {e}")
        return ""


def _process_docx(file_content: bytes) -> str:
    """Extract text from DOCX file."""
    try:
        from docx import Document
        doc = Document(BytesIO(file_content))
        text_parts = []
        for para in doc.paragraphs:
            if para.text.strip():
                text_parts.append(para.text)
        return "\n".join(text_parts)
    except ImportError:
        logger.warning("python-docx not installed. Install it for DOCX support: pip install python-docx")
        return "[DOCX content - python-docx not installed]"
    except Exception as e:
        logger.error(f"Error extracting DOCX: {e}")
        return ""
