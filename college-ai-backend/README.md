# Learnix - RAG-based AI Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that answers questions from pre-uploaded documents using embeddings, vector search, and the Gemini API.

## Features

- 📄 **Document Upload**: Support for PDF, DOCX, and TXT files
- 🔍 **Semantic Search**: Find relevant content using vector embeddings
- 🤖 **AI-Powered Answers**: Generate contextual responses using Gemini API
- 💬 **Chat Interface**: Clean, responsive web UI
- 🎯 **Mock Mode**: Run without heavy dependencies for quick testing
- 🔧 **Modular Design**: Easy to swap components (Qdrant, embeddings, LLM)

## Quick Start (Mock Mode)

Run the project without heavy dependencies for immediate testing:

### 1. Create Virtual Environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install Minimal Dependencies

```powershell
pip install -r requirements.txt
```

### 3. Start the Server

```powershell
uvicorn app:app --reload --port 8000
```

### 4. Open in Browser

Navigate to: http://localhost:8000

The mock mode will:
- Generate deterministic embeddings (no ML models needed)
- Use in-memory vector search
- Return mock responses (no Gemini API required)

## Full Production Setup

### 1. Install All Dependencies

Uncomment the optional packages in `requirements.txt` and install:

```powershell
pip install sentence-transformers qdrant-client transformers PyPDF2 python-docx google-generativeai
```

### 2. Set Up Qdrant (Optional)

Run Qdrant locally with Docker:

```powershell
docker run -p 6333:6333 qdrant/qdrant
```

Or use Qdrant Cloud: https://cloud.qdrant.io

### 3. Configure Environment

Copy `.env.example` to `.env` and set:

```env
USE_MOCKS=0
GEMINI_API_KEY=your_actual_api_key
QDRANT_URL=http://localhost:6333
```

### 4. Run Production Server

```powershell
uvicorn app:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### Health Check
```
GET /api/health
```

### Upload Document
```
POST /api/upload/
Content-Type: multipart/form-data
Body: file=@document.pdf
```

### Ask Question
```
POST /api/ask/
Content-Type: application/x-www-form-urlencoded
Body: question=What is the main topic?&top_k=5
```

### List Documents
```
GET /api/documents/
```

### Download Document
```
GET /api/download/{filename}
```

## Project Structure

```
college-ai-backend/
├── app.py                      # FastAPI application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── README.md                  # This file
├── data/                      # Uploaded documents storage
├── frontend/                  # Static web UI
│   ├── index.html
│   ├── app.js
│   └── styles.css
└── utils/                     # Core modules
    ├── __init__.py
    ├── embeddings.py          # Embedding generation (mock/real)
    ├── loader.py              # Document processing
    ├── rag.py                 # Vector search (in-memory/Qdrant)
    └── gemini.py              # LLM integration (mock/real)
```

## Technology Stack

- **Backend**: FastAPI
- **Frontend**: Vanilla JavaScript (HTML/CSS/JS)
- **Embeddings**: Sentence Transformers (Hugging Face)
- **Vector DB**: Qdrant (or in-memory fallback)
- **LLM**: Google Gemini API
- **Document Processing**: PyPDF2, python-docx

## Testing with curl

### Upload a document:
```powershell
curl -X POST "http://127.0.0.1:8000/api/upload/" -F "file=@C:\path\to\document.pdf"
```

### Ask a question:
```powershell
curl -X POST "http://127.0.0.1:8000/api/ask/" -d "question=What is this document about?" -d "top_k=5"
```

## Customization

### Use Real Embeddings
Edit `utils/embeddings.py` - set `USE_MOCKS=0` and ensure sentence-transformers is installed.

### Use Qdrant
Edit `utils/rag.py` - swap `InMemoryIndex` with `QdrantIndex` implementation.

### Use Real Gemini API
Edit `utils/gemini.py` - set `USE_MOCKS=0` and provide `GEMINI_API_KEY`.

## Troubleshooting

**Issue**: Heavy packages fail to install on Windows
**Solution**: Use mock mode or install Visual C++ Build Tools

**Issue**: Qdrant connection fails
**Solution**: Verify Qdrant is running: `docker ps` or check cloud dashboard

**Issue**: Gemini API errors
**Solution**: Verify API key and check quota limits

## License

MIT License - feel free to use for educational purposes.
