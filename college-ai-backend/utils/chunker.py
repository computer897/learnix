"""
Text chunking utilities for splitting large documents.
"""

from typing import List
import re


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """
    Split text into overlapping chunks.
    
    Args:
        text: The text to chunk
        chunk_size: Maximum size of each chunk (in characters)
        overlap: Number of characters to overlap between chunks
        
    Returns:
        List of text chunks
    """
    if not text or len(text) == 0:
        return []
    
    # Clean up excessive whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        
        # If this is not the last chunk, try to break at a sentence or word boundary
        if end < len(text):
            # Look for sentence boundaries (., !, ?)
            sentence_end = max(
                text.rfind('. ', start, end),
                text.rfind('! ', start, end),
                text.rfind('? ', start, end)
            )
            
            if sentence_end > start + chunk_size // 2:  # Only break if we found a good spot
                end = sentence_end + 1
            else:
                # Fall back to word boundary
                space_pos = text.rfind(' ', start, end)
                if space_pos > start:
                    end = space_pos
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        # Move start position, accounting for overlap
        start = end - overlap
        if start <= 0:
            start = end
    
    return chunks


def chunk_by_paragraphs(text: str, max_chunk_size: int = 1000) -> List[str]:
    """
    Split text by paragraphs, combining small paragraphs into chunks.
    
    Args:
        text: The text to chunk
        max_chunk_size: Maximum size of each chunk
        
    Returns:
        List of text chunks
    """
    # Split by double newline (paragraphs)
    paragraphs = re.split(r'\n\s*\n', text)
    
    chunks = []
    current_chunk = []
    current_size = 0
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        
        para_size = len(para)
        
        # If adding this paragraph exceeds max size, save current chunk
        if current_size + para_size > max_chunk_size and current_chunk:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
            current_size = 0
        
        # If a single paragraph is larger than max size, split it
        if para_size > max_chunk_size:
            if current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = []
                current_size = 0
            
            # Split large paragraph
            chunks.extend(chunk_text(para, max_chunk_size, 100))
        else:
            current_chunk.append(para)
            current_size += para_size
    
    # Add remaining chunk
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks
