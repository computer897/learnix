# Learnix Quick Reference - Visual Guide

## 🎯 One-Page Overview

### The RAG Pipeline (Simplified)

```mermaid
graph LR
    A[📄 Upload PDF] -->|Extract Text| B[✂️ Split Chunks]
    B -->|Embed| C[🧠 Vector DB]
    D[❓ Your Question] -->|Embed| E[🔍 Search]
    C --> E
    E -->|Context| F[🤖 Gemini AI]
    F --> G[✨ Answer]
    
    style A fill:#4a90e2,color:#fff
    style C fill:#7ed321,color:#fff
    style F fill:#d0021b,color:#fff
    style G fill:#f5a623,color:#fff
```

---

## 📊 3-Second Summary

```mermaid
graph TB
    Upload["1️⃣ Upload Documents"] --> Search["2️⃣ Ask Questions"]
    Search --> Answer["3️⃣ Get Smart Answers"]
    
    style Upload fill:#e1f5ff
    style Search fill:#fff4e1
    style Answer fill:#e1ffe1
```

---

## 🔄 Request Flow (Detailed)

```mermaid
sequenceDiagram
    User->>+API: "What is OOP?"
    API->>+Embedder: Embed question
    Embedder-->>-API: Vector [0.2, 0.5, ...]
    API->>+VectorDB: Find similar
    VectorDB-->>-API: Top 5 chunks
    API->>+Gemini: Question + Context
    Gemini-->>-API: Detailed answer
    API-->>-User: Display response
```

---

## 💾 Data Storage Structure

```mermaid
graph TD
    subgraph Storage["In-Memory Index"]
        V1[Vector 1<br/>384 dims]
        V2[Vector 2<br/>384 dims]
        V3[Vector N<br/>384 dims]
    end
    
    subgraph Metadata["Document Info"]
        M1[Chunk Text]
        M2[Source File]
        M3[Page Number]
    end
    
    V1 -.-> M1
    V2 -.-> M2
    V3 -.-> M3
    
    style Storage fill:#e1ffe1
    style Metadata fill:#e1f5ff
```

---

## ⚙️ Core Components

```mermaid
graph TB
    subgraph Frontend
        UI[HTML/CSS/JS]
    end
    
    subgraph Backend
        FastAPI[FastAPI Server]
    end
    
    subgraph ML
        ST[Sentence<br/>Transformers]
        Gemini[Gemini<br/>API]
    end
    
    UI <--> FastAPI
    FastAPI <--> ST
    FastAPI <--> Gemini
    
    style Frontend fill:#4a90e2,color:#fff
    style Backend fill:#f5a623,color:#fff
    style ML fill:#9013fe,color:#fff
```

---

## 📈 Performance Breakdown

```mermaid
pie title Response Time Distribution
    "Question Embedding" : 5
    "Vector Search" : 10
    "Gemini Generation" : 75
    "Response Formatting" : 10
```

---

## 🔐 Security Model

```mermaid
graph LR
    Docs[Your Documents] -->|Stored| Local[Local Machine]
    Local -->|Embeddings Only| Memory[RAM]
    Query[Your Question] -->|API Call| Gemini[Gemini Cloud]
    
    Note1[Docs never leave<br/>your computer] -.-> Local
    Note2[Only embeddings<br/>in memory] -.-> Memory
    Note3[No query storage<br/>by Google] -.-> Gemini
    
    style Docs fill:#e1ffe1
    style Local fill:#fff4e1
    style Gemini fill:#e1f5ff
```

---

## 🎓 User Journey

```mermaid
journey
    title Daily Study Session
    section Setup (One-time)
      Upload OOPS Notes: 5: Student
      Upload Java Notes: 5: Student
      System Indexes: 3: System
    section Study
      Ask Question: 5: Student
      Get Answer: 5: Student
      Read & Learn: 5: Student
      Ask Follow-up: 5: Student
```

---

## 🛠️ Technology Matrix

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **UI** | HTML/CSS/JS | Chat interface |
| **Server** | FastAPI | REST API |
| **Embedding** | all-MiniLM-L6-v2 | Text → Vectors |
| **Storage** | In-Memory Index | Fast retrieval |
| **LLM** | Gemini 1.5 Flash | Answer generation |
| **PDF** | PyPDF2 | Text extraction |

---

## ⚡ Quick Commands

### Start Server
```bash
cd college-ai-backend
uvicorn app:app --host 127.0.0.1 --port 8000
```

### Access App
```
http://127.0.0.1:8000
```

### API Health Check
```bash
curl http://127.0.0.1:8000/api/health
```

---

## 📝 API Endpoints

```mermaid
graph TD
    Root["/"] -->|GET| UI[Frontend UI]
    API["/api"] --> Health["/health"]
    API --> Ask["/ask POST"]
    API --> Upload["/upload POST"]
    API --> Docs["/documents GET"]
    API --> Download["/download/{file} GET"]
    
    style Root fill:#4a90e2,color:#fff
    style Ask fill:#f5a623,color:#fff
    style Upload fill:#7ed321,color:#fff
```

---

## 🎯 Best Practices

### ✅ DO
- Upload course-specific PDFs
- Ask detailed questions
- Use technical terms from your course
- Review source citations

### ❌ DON'T
- Ask about topics not in your docs
- Use extremely vague questions
- Expect answers without uploading materials
- Upload non-text PDFs (images only)

---

## 🐛 Quick Troubleshooting

```mermaid
flowchart TD
    Issue{What's wrong?}
    
    Issue -->|Server won't start| Port[Port 8000 busy?<br/>Kill process]
    Issue -->|No answers| Docs[Upload documents<br/>first]
    Issue -->|Slow response| Model[Embedding model<br/>downloading]
    Issue -->|Generic answers| Context[No relevant docs<br/>found]
    
    Port --> Fix1[netstat -ano]
    Docs --> Fix2[Click upload]
    Model --> Fix3[Wait 2-3 min]
    Context --> Fix4[Upload better docs]
    
    style Issue fill:#d0021b,color:#fff
    style Fix1 fill:#7ed321,color:#fff
    style Fix2 fill:#7ed321,color:#fff
    style Fix3 fill:#7ed321,color:#fff
    style Fix4 fill:#7ed321,color:#fff
```

---

## 📚 File Structure (Simplified)

```
learnix/
├── assets/diagrams/      ← You are here
├── college-ai-backend/
│   ├── app.py           ← Main server
│   ├── frontend/        ← UI files
│   │   ├── index.html
│   │   ├── about.html
│   │   └── styles.css
│   ├── utils/           ← Core logic
│   │   ├── rag.py       ← RAG pipeline
│   │   ├── embeddings.py
│   │   └── gemini.py
│   └── data/            ← Your PDFs
└── README.md            ← Start here
```

---

## 🚀 From Zero to Answers

```mermaid
stateDiagram-v2
    [*] --> Install: pip install -r requirements.txt
    Install --> Configure: Add GEMINI_API_KEY to .env
    Configure --> Start: uvicorn app:app
    Start --> Upload: Upload PDFs via UI
    Upload --> Ready: System indexes docs
    Ready --> Ask: Type your question
    Ask --> Answer: Receive AI response
    Answer --> Ask: Ask more questions
    Answer --> [*]: Done studying
```

---

## 💡 Key Concepts

### Embeddings
Converting text to numbers that capture meaning:
```
"Object Oriented Programming" 
→ [0.23, -0.45, 0.67, ..., 0.12] (384 numbers)
```

### Cosine Similarity
How similar two vectors are (0-1 scale):
```
Question vector ⋅ Document vector = Similarity Score
Higher score = More relevant
```

### RAG
Retrieval + Generation = Accurate Answers:
```
Your Docs → Find Relevant → AI Generate → Answer
```

---

## 🎨 Color Legend

Throughout these diagrams:
- 🔵 **Blue** (`#4a90e2`) = User/Frontend
- 🟠 **Orange** (`#f5a623`) = Backend/API
- 🟢 **Green** (`#7ed321`) = Storage/Data
- 🟣 **Purple** (`#9013fe`) = ML/AI
- 🔴 **Red** (`#d0021b`) = External Services

---

## 📞 Need Help?

1. **Check**: [Full Documentation](../../README.md)
2. **Read**: [How It Works](how-it-works.md)
3. **Review**: [Architecture](system-architecture.md)
4. **Debug**: [Data Flow](data-flow.md)

---

**Print this page for quick reference! 📄**

*Last updated: October 27, 2025*
