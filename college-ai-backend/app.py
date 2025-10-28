import os
from pathlib import Path
from typing import List
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from utils.loader import process_file
from utils.embeddings import get_embedding, embed_query
from utils.rag import InMemoryIndex
from utils.gemini import generate_answer_from_context
from utils.storage import DocumentStorage
from utils.chunker import chunk_text
from utils.chat_history import ChatHistory

APP_DIR = Path(__file__).parent
DATA_DIR = APP_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Secure storage folder for uploads (not publicly accessible)
STORAGE_DIR = APP_DIR / "storage" / "uploads"
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

# Initialize document storage
storage = DocumentStorage(DATA_DIR)

# Initialize chat history
chat_history = ChatHistory(APP_DIR / "storage")

app = FastAPI(title="Learnix - College AI Assistant")

# CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple in-memory index used when Qdrant isn't configured
index = InMemoryIndex()

@app.on_event("startup")
async def startup_event():
    """Load existing documents and embeddings on startup."""
    # Reload all existing documents into the index
    all_docs = storage.get_all_documents()
    loaded_count = 0
    total_chunks = 0
    
    for doc_metadata in all_docs:
        doc_hash = doc_metadata["hash"]
        filename = doc_metadata["filename"]
        text = storage.get_document_text(doc_hash)
        
        if text:
            # Split into chunks for better retrieval
            chunks = chunk_text(text, chunk_size=1000, overlap=200)
            logger.info(f"Loading {filename}: {len(chunks)} chunks")
            
            for i, chunk in enumerate(chunks):
                # Create unique ID for each chunk
                chunk_id = f"{doc_hash}_chunk_{i}"
                embedding = get_embedding(chunk)
                index.add_document(chunk_id, chunk, embedding)
                total_chunks += 1
            
            loaded_count += 1
    
    print(f"✅ Loaded {loaded_count} documents ({total_chunks} chunks) into the index")


@app.get("/api/health")
def health():
    return {"status": "ok", "mode": "mock" if os.getenv("USE_MOCKS", "1") == "1" else "production"}


@app.post("/api/upload/")
async def upload_file(file: UploadFile = File(...)):
    """Upload and process a document with duplicate detection."""
    try:
        content = await file.read()
        logger.info(f"Uploading file: {file.filename}, size: {len(content)} bytes")
        
        # Check if document already exists
        doc_hash = storage.get_document_hash(content)
        if storage.document_exists(doc_hash):
            logger.info(f"Duplicate detected: {file.filename}")
            return {
                "message": f"{file.filename} already uploaded (duplicate detected)",
                "filename": file.filename,
                "status": "duplicate"
            }
        
        # Extract and clean text
        logger.info(f"Processing file: {file.filename}")
        text = process_file(file.filename, content)
        if not text:
            logger.warning(f"No text extracted from: {file.filename}")
            raise HTTPException(status_code=400, detail="No text extracted from file")

        logger.info(f"Extracted {len(text)} characters from {file.filename}")
        
        # Split into chunks for better retrieval
        chunks = chunk_text(text, chunk_size=1000, overlap=200)
        logger.info(f"Split into {len(chunks)} chunks")

        # Save to persistent storage (save full text)
        logger.info(f"Saving to persistent storage: {file.filename}")
        # We save a dummy embedding for the full document
        metadata = storage.save_document(file.filename, content, text, [])
        
        # Add chunks to search index
        logger.info(f"Adding {len(chunks)} chunks to search index")
        for i, chunk in enumerate(chunks):
            chunk_id = f"{metadata['hash']}_chunk_{i}"
            chunk_embedding = get_embedding(chunk)
            index.add_document(chunk_id, chunk, chunk_embedding)

        logger.info(f"Successfully uploaded: {file.filename}")
        return {
            "message": f"{file.filename} uploaded and indexed successfully!",
            "filename": file.filename,
            "status": "new",
            "doc_hash": metadata["hash"]
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading {file.filename}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@app.post("/api/ask/")
async def ask_question(question: str = Form(...), top_k: int = Form(10)):
    if not question:
        raise HTTPException(status_code=400, detail="Question is required")

    # Get query embedding
    q_emb = embed_query(question)

    # Retrieve relevant docs (get more chunks for better context)
    hits = index.query(q_emb, top_k=top_k)

    context_texts: List[str] = [h["text"] for h in hits]

    # Call Gemini (or mock) to generate answer
    answer = generate_answer_from_context(question, context_texts)
    
    # Get source IDs (chunk identifiers, not file paths)
    source_ids = [h["id"] for h in hits]
    
    # Save to chat history
    chat_history.add_message(question, answer, source_ids)

    return JSONResponse({"answer": answer, "sources": source_ids})


@app.get("/api/documents/")
def list_documents():
    """List all uploaded documents with metadata."""
    docs = storage.get_all_documents()
    return {
        "documents": [
            {
                "name": doc["filename"],
                "uploaded_at": doc["uploaded_at"],
                "text_length": doc["text_length"]
            }
            for doc in docs
        ],
        "total": len(docs)
    }


@app.get("/api/download/{filename}")
def download_file(filename: str):
    path = DATA_DIR / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path)


# Chat History Endpoints
@app.get("/api/chat/history")
def get_chat_history(limit: int = 20):
    """Get recent chat history."""
    history = chat_history.get_history(limit=limit)
    return JSONResponse({"history": history, "count": len(history)})


@app.delete("/api/chat/history")
def clear_chat_history():
    """Clear all chat history."""
    success = chat_history.clear_history()
    if success:
        return JSONResponse({"message": "Chat history cleared successfully"})
    else:
        raise HTTPException(status_code=500, detail="Failed to clear chat history")


@app.delete("/api/chat/message/{message_id}")
def delete_message(message_id: str):
    """Delete a specific message from history."""
    success = chat_history.delete_message(message_id)
    if success:
        return JSONResponse({"message": "Message deleted successfully"})
    else:
        raise HTTPException(status_code=404, detail="Message not found")


@app.get("/api/chat/stats")
def get_chat_stats():
    """Get chat history statistics."""
    stats = chat_history.get_stats()
    return JSONResponse(stats)


# Mount frontend static files LAST (after all API routes)
# This must be last because it uses catch-all routing
static_dir = APP_DIR / "frontend"
if static_dir.exists():
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="frontend")
