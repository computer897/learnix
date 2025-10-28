import os
import re
from typing import List
from PyPDF2 import PdfReader
from docx import Document

# -----------------------------------------------
# Text Processor for Learnix
# -----------------------------------------------
# Responsibilities:
# 1. Extract text from PDF, DOCX, or TXT files
# 2. Clean unwanted elements (page numbers, line breaks)
# 3. Split text into semantically meaningful chunks
# -----------------------------------------------


def extract_text(file_path: str) -> str:
    """Extract plain text from supported document formats."""
    text = ""
    extension = os.path.splitext(file_path)[-1].lower()

    try:
        if extension == ".pdf":
            reader = PdfReader(file_path)
            for page in reader.pages:
                content = page.extract_text()
                if content:
                    text += content + " "
        elif extension == ".docx":
            doc = Document(file_path)
            for para in doc.paragraphs:
                text += para.text + " "
        elif extension == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
        else:
            raise ValueError(f"Unsupported file format: {extension}")

    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return ""

    return clean_text(text)


def clean_text(text: str) -> str:
    """Remove page numbers, excessive whitespace, and non-printable characters."""
    if not text:
        return ""
    text = re.sub(r'\bPage\s*\d+\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+', ' ', text)
    text = text.encode("ascii", "ignore").decode()  # remove special chars
    return text.strip()


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Split large text into overlapping chunks for embedding generation.
    Each chunk has slight overlap with the previous to preserve context.
    """
    if not text:
        return []

    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap  # slide window
        if end == len(words):
            break

    return chunks


# Example usage (for testing standalone):
if __name__ == "__main__":
    test_path = "sample.pdf"
    if os.path.exists(test_path):
        txt = extract_text(test_path)
        parts = chunk_text(txt)
        print(f"✅ Extracted {len(parts)} chunks from {test_path}")
    else:
        print("⚠️ sample.pdf not found.")
