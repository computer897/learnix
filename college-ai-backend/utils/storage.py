"""
Persistent storage module for documents.

Saves document text, metadata, and handles document persistence
across server restarts.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional
import hashlib
from datetime import datetime

class DocumentStorage:
    """Manages persistent storage of document metadata and content."""
    
    def __init__(self, storage_dir: Path):
        self.storage_dir = storage_dir
        self.storage_dir.mkdir(exist_ok=True)
        self.metadata_file = storage_dir / "documents_metadata.json"
        self.documents: Dict[str, Dict] = self._load_metadata()
    
    def _load_metadata(self) -> Dict[str, Dict]:
        """Load document metadata from disk."""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _save_metadata(self):
        """Save document metadata to disk."""
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(self.documents, f, indent=2, ensure_ascii=False)
    
    def get_document_hash(self, content: bytes) -> str:
        """Generate a hash for document content to detect duplicates."""
        return hashlib.sha256(content).hexdigest()
    
    def document_exists(self, doc_hash: str) -> bool:
        """Check if a document with this hash already exists."""
        return doc_hash in self.documents
    
    def save_document(self, filename: str, content: bytes, text: str, embedding: list) -> Dict:
        """
        Save document with its content, text, and metadata.
        
        Returns document metadata dictionary.
        """
        doc_hash = self.get_document_hash(content)
        
        # Check if already exists
        if self.document_exists(doc_hash):
            return self.documents[doc_hash]
        
        # Save original file
        file_path = self.storage_dir / filename
        with open(file_path, 'wb') as f:
            f.write(content)
        
        # Save extracted text
        text_path = self.storage_dir / f"{doc_hash}.txt"
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        # Save metadata
        metadata = {
            "filename": filename,
            "hash": doc_hash,
            "file_path": str(file_path),
            "text_path": str(text_path),
            "uploaded_at": datetime.now().isoformat(),
            "text_length": len(text),
            "embedding_dim": len(embedding) if embedding is not None else 0
        }
        
        self.documents[doc_hash] = metadata
        self._save_metadata()
        
        return metadata
    
    def get_all_documents(self) -> List[Dict]:
        """Get list of all stored documents."""
        return list(self.documents.values())
    
    def get_document_text(self, doc_hash: str) -> Optional[str]:
        """Retrieve the stored text for a document."""
        if doc_hash not in self.documents:
            return None
        
        text_path = Path(self.documents[doc_hash]["text_path"])
        if text_path.exists():
            with open(text_path, 'r', encoding='utf-8') as f:
                return f.read()
        return None
    
    def delete_document(self, doc_hash: str) -> bool:
        """Delete a document and its associated files."""
        if doc_hash not in self.documents:
            return False
        
        metadata = self.documents[doc_hash]
        
        # Delete files
        for path_key in ["file_path", "text_path"]:
            path = Path(metadata.get(path_key, ""))
            if path.exists():
                path.unlink()
        
        # Remove from metadata
        del self.documents[doc_hash]
        self._save_metadata()
        
        return True
