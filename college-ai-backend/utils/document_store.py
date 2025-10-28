import os
import hashlib
from typing import List, Dict
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from sentence_transformers import SentenceTransformer

# ---------- Configuration ----------
QDRANT_URL = os.getenv("QDRANT_URL", "https://4fd42f5a-a902-4b9e-b4b2-79f82eebf981.us-east4-0.gcp.cloud.qdrant.io")
COLLECTION_NAME = "learnix_documents"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
UPLOAD_FOLDER = "uploads"

# ---------- Setup Clients ----------
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
qdrant = QdrantClient(url=QDRANT_URL)
model = SentenceTransformer(EMBEDDING_MODEL_NAME)


# ---------- Helper Functions ----------
def clean_text(text: str) -> str:
    """Remove unwanted characters, page numbers, and formatting."""
    import re
    text = re.sub(r'\bPage\s*\d+\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def get_file_hash(filename: str) -> str:
    """Generate unique hash for each file to avoid duplication."""
    return hashlib.md5(filename.encode()).hexdigest()


def ensure_collection_exists():
    """Create the Qdrant collection if not exists."""
    existing_collections = [c.name for c in qdrant.get_collections().collections]
    if COLLECTION_NAME not in existing_collections:
        qdrant.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )


# ---------- Main Functions ----------

def store_document(file_path: str, file_name: str):
    """Extract text, generate embeddings, and store them persistently."""
    from PyPDF2 import PdfReader

    ensure_collection_exists()

    # 1. Extract text
    text = ""
    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() or ""
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

    text = clean_text(text)
    if not text:
        return {"error": "No text found in document"}

    # 2. Split text into chunks
    chunk_size = 500
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    # 3. Generate embeddings
    embeddings = model.encode(chunks).tolist()

    # 4. Store in Qdrant
    file_hash = get_file_hash(file_name)
    points = [
        PointStruct(
            id=int(hashlib.md5(f"{file_hash}_{i}".encode()).hexdigest(), 16) % (10**12),
            vector=embeddings[i],
            payload={"text": chunks[i], "file": file_name}
        )
        for i in range(len(chunks))
    ]

    qdrant.upsert(collection_name=COLLECTION_NAME, points=points)

    return {"message": f"Stored {len(chunks)} chunks from {file_name} successfully."}


def retrieve_context(query: str, top_k: int = 3) -> List[str]:
    """Retrieve top matching chunks for a given query."""
    ensure_collection_exists()
    query_vector = model.encode([query])[0].tolist()

    results = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k
    )

    contexts = [r.payload["text"] for r in results if "text" in r.payload]
    return contexts


def load_existing_documents() -> List[Dict]:
    """Check what documents already exist in the store."""
    ensure_collection_exists()
    points = qdrant.scroll(collection_name=COLLECTION_NAME, limit=1000)
    return [p.payload for p in points[0] if p.payload]


# ---------- Initialize on Startup ----------
ensure_collection_exists()
print("✅ Document store initialized and ready.")
