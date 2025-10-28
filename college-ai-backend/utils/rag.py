"""
RAG (Retrieval-Augmented Generation) implementation.

Provides an in-memory vector index for mock/dev mode.
Can be extended to use Qdrant for production.
"""

import numpy as np
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class InMemoryIndex:
    """
    Simple in-memory vector index using cosine similarity.
    
    Good for development and testing. For production with large datasets,
    replace with QdrantIndex or similar vector database.
    """
    
    def __init__(self):
        self.docs: List[Dict] = []  # {"id": str, "text": str, "emb": np.array}
    
    def add_document(self, doc_id: str, text: str, embedding: np.ndarray):
        """
        Add a document to the index.
        
        Args:
            doc_id: Unique identifier for the document
            text: Full text content
            embedding: Vector embedding of the text
        """
        emb = np.array(embedding, dtype=np.float32)
        # Normalize embedding
        emb = emb / (np.linalg.norm(emb) + 1e-8)
        
        self.docs.append({
            "id": doc_id,
            "text": text,
            "emb": emb
        })
        logger.info(f"Added document to index: {doc_id}")
    
    def query(self, query_embedding: np.ndarray, top_k: int = 5) -> List[Dict]:
        """
        Query the index for similar documents.
        
        Args:
            query_embedding: Vector embedding of the query
            top_k: Number of results to return
            
        Returns:
            List of dicts with keys: id, text, score
        """
        if not self.docs:
            logger.warning("Index is empty - no documents to search")
            return []
        
        q = np.array(query_embedding, dtype=np.float32)
        q = q / (np.linalg.norm(q) + 1e-8)
        
        # Compute cosine similarity with all documents
        embs = np.stack([d["emb"] for d in self.docs], axis=0)
        similarities = embs @ q  # Already normalized, so dot product = cosine sim
        
        # Get top K results
        top_idx = np.argsort(-similarities)[:top_k]
        
        results = []
        for i in top_idx:
            results.append({
                "id": self.docs[i]["id"],
                "text": self.docs[i]["text"],
                "score": float(similarities[i])
            })
        
        logger.info(f"Query returned {len(results)} results")
        return results
    
    def get_document_count(self) -> int:
        """Get the number of documents in the index."""
        return len(self.docs)
    
    def clear(self):
        """Clear all documents from the index."""
        self.docs.clear()
        logger.info("Index cleared")


class QdrantIndex:
    """
    Qdrant-based vector index for production use.
    
    TODO: Implement when USE_MOCKS=0 and Qdrant is configured.
    """
    
    def __init__(self, url: str, api_key: Optional[str] = None, collection_name: str = "learnix"):
        """
        Initialize Qdrant client.
        
        Args:
            url: Qdrant server URL
            api_key: Optional API key for authentication
            collection_name: Name of the collection to use
        """
        try:
            from qdrant_client import QdrantClient
            from qdrant_client.models import Distance, VectorParams
            
            self.client = QdrantClient(url=url, api_key=api_key)
            self.collection_name = collection_name
            
            # Create collection if it doesn't exist
            collections = self.client.get_collections().collections
            if collection_name not in [c.name for c in collections]:
                self.client.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
                )
                logger.info(f"Created Qdrant collection: {collection_name}")
            
        except ImportError:
            raise ImportError("qdrant-client not installed. Install it: pip install qdrant-client")
    
    def add_document(self, doc_id: str, text: str, embedding: np.ndarray):
        """Add document to Qdrant."""
        # TODO: Implement Qdrant upsert
        raise NotImplementedError("QdrantIndex not yet implemented")
    
    def query(self, query_embedding: np.ndarray, top_k: int = 5) -> List[Dict]:
        """Query Qdrant for similar documents."""
        # TODO: Implement Qdrant search
        raise NotImplementedError("QdrantIndex not yet implemented")
