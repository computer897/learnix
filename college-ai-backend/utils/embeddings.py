"""
Embeddings helper module.

In mock mode (USE_MOCKS=1), generates deterministic pseudo-embeddings.
In production mode (USE_MOCKS=0), uses sentence-transformers for real embeddings.
"""

import os
import numpy as np
import logging

logger = logging.getLogger(__name__)

USE_MOCKS = os.getenv("USE_MOCKS", "1") == "1"
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

_embedding_model = None


def _load_model():
    """Load the sentence-transformers model (lazy initialization)."""
    global _embedding_model
    
    if _embedding_model is not None:
        return _embedding_model
    
    if USE_MOCKS:
        logger.info("Running in MOCK mode - using deterministic embeddings")
        return None
    
    try:
        from sentence_transformers import SentenceTransformer
        logger.info(f"Loading embedding model: {EMBEDDING_MODEL}")
        _embedding_model = SentenceTransformer(EMBEDDING_MODEL)
        logger.info("✅ Successfully loaded sentence-transformers model")
        return _embedding_model
    except ImportError as e:
        logger.warning(f"sentence-transformers not available: {e}. Using fallback embeddings.")
        return None
    except Exception as e:
        logger.error(f"Error loading embedding model: {e}. Using fallback embeddings.")
        return None


def _text_to_mock_vector(text: str, dim: int = 384) -> np.ndarray:
    """
    Generate deterministic pseudo-embedding from text.
    
    Uses hash of text to create reproducible vectors - same text always
    produces the same embedding.
    """
    # Use hash for deterministic random seed
    h = abs(hash(text)) % (10**9)
    rng = np.random.RandomState(h)
    v = rng.rand(dim).astype(np.float32)
    # Normalize to unit vector
    v = v / (np.linalg.norm(v) + 1e-8)
    return v


def get_embedding(text: str) -> np.ndarray:
    """
    Generate embedding for a text document.
    
    Args:
        text: Input text to embed
        
    Returns:
        Numpy array of embedding vector
    """
    if not text or not text.strip():
        # Return zero vector for empty text
        return np.zeros(384, dtype=np.float32)
    
    model = _load_model()
    
    if model:
        # Real embedding using sentence-transformers
        embedding = model.encode([text])[0].astype(np.float32)
        return embedding
    else:
        # Mock embedding
        return _text_to_mock_vector(text)


def embed_query(text: str) -> np.ndarray:
    """
    Generate embedding for a query.
    
    Same as get_embedding but kept as separate function for clarity
    and potential future query-specific optimizations.
    
    Args:
        text: Query text to embed
        
    Returns:
        Numpy array of embedding vector
    """
    return get_embedding(text)


def get_embedding_dimension() -> int:
    """Get the dimensionality of embeddings."""
    model = _load_model()
    if model:
        # Get actual model dimension
        return model.get_sentence_embedding_dimension()
    else:
        # Mock dimension
        return 384
