# Learnix System Architecture

## Complete System Overview

```mermaid
graph TB
    subgraph Frontend["Frontend Layer"]
        UI[User Interface<br/>Chat Interface]
        Upload[Document Upload UI]
    end
    
    subgraph Backend["Backend Layer (FastAPI)"]
        API[REST API Endpoints<br/>/api/ask, /api/upload]
        DocProcessor[Document Processor<br/>PDF Text Extraction]
        Chunker[Text Chunker<br/>1000 chars, 200 overlap]
    end
    
    subgraph Embedding["Embedding Pipeline"]
        EmbedModel[Sentence Transformers<br/>all-MiniLM-L6-v2<br/>384-dim vectors]
    end
    
    subgraph Storage["Vector Storage"]
        InMemory[In-Memory Index<br/>Cosine Similarity Search]
    end
    
    subgraph LLM["AI Generation"]
        Gemini[Google Gemini API<br/>gemini-1.5-flash]
    end
    
    UI -->|User Query| API
    Upload -->|PDF Upload| API
    API -->|Extract Text| DocProcessor
    DocProcessor -->|Raw Text| Chunker
    Chunker -->|Text Chunks| EmbedModel
    EmbedModel -->|Embeddings| InMemory
    
    API -->|Question| EmbedModel
    EmbedModel -->|Query Embedding| InMemory
    InMemory -->|Top-K Context| API
    API -->|Prompt + Context| Gemini
    Gemini -->|Generated Answer| API
    API -->|Response| UI
    
    style Frontend fill:#e1f5ff
    style Backend fill:#fff4e1
    style Embedding fill:#f0e1ff
    style Storage fill:#e1ffe1
    style LLM fill:#ffe1e1
```

## Technology Stack

```mermaid
graph LR
    subgraph Client
        HTML[HTML/CSS/JS<br/>Vanilla Frontend]
    end
    
    subgraph Server
        FastAPI[FastAPI<br/>Python 3.10+]
        Uvicorn[Uvicorn<br/>ASGI Server]
    end
    
    subgraph ML
        HF[HuggingFace<br/>Transformers]
        ST[Sentence<br/>Transformers]
    end
    
    subgraph External
        GeminiAPI[Google Gemini<br/>1.5 Flash]
    end
    
    HTML --> FastAPI
    FastAPI --> Uvicorn
    FastAPI --> HF
    HF --> ST
    FastAPI --> GeminiAPI
    
    style Client fill:#4a90e2
    style Server fill:#f5a623
    style ML fill:#7ed321
    style External fill:#d0021b
```

## Component Details

### Frontend
- **Technology**: Vanilla HTML, CSS, JavaScript
- **Features**: 
  - Chat interface with message history
  - PDF document upload
  - Dark/Light theme toggle
  - Real-time response streaming

### Backend (FastAPI)
- **Port**: 8000 (127.0.0.1)
- **Key Endpoints**:
  - `POST /api/ask` - Question answering
  - `POST /api/upload/` - Document upload
  - `GET /api/documents/` - List uploaded documents
  - `GET /api/download/{filename}` - Download documents
  - `GET /api/health` - Health check

### Document Processing Pipeline
1. **PDF Upload** → User uploads course materials
2. **Text Extraction** → PyPDF2 extracts text from PDFs
3. **Chunking** → Text split into 1000-char chunks with 200-char overlap
4. **Embedding** → Each chunk converted to 384-dim vector
5. **Storage** → Vectors stored in in-memory index

### Embedding Model
- **Model**: sentence-transformers/all-MiniLM-L6-v2
- **Dimensions**: 384
- **Device**: CPU (optimized for speed)
- **Purpose**: Convert text to semantic vectors

### Vector Search
- **Type**: In-Memory Index
- **Algorithm**: Cosine Similarity
- **Top-K**: Retrieves 5 most relevant chunks
- **Normalization**: L2 normalized embeddings

### LLM Integration
- **Model**: Google Gemini 1.5 Flash
- **Temperature**: 0.7 (balanced creativity)
- **Max Tokens**: 2048
- **Context Window**: Enhanced with retrieved documents
- **Prompt Engineering**: Comprehensive answer formatting
