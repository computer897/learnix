# How Learnix Works

## Overview

Learnix is an AI-powered study assistant that helps students get comprehensive answers from their course materials using Retrieval-Augmented Generation (RAG).

## Simple Visual Explanation

```mermaid
graph LR
    A[📚 Upload<br/>Course PDFs] --> B[🔪 Split into<br/>Small Chunks]
    B --> C[🧠 Convert to<br/>Vector Embeddings]
    C --> D[💾 Store in<br/>Vector Index]
    
    E[❓ Ask a<br/>Question] --> F[🔍 Find Relevant<br/>Chunks]
    D --> F
    F --> G[🤖 Generate Answer<br/>with Gemini AI]
    G --> H[✨ Get Comprehensive<br/>Answer]
    
    style A fill:#4a90e2,color:#fff
    style B fill:#f5a623,color:#fff
    style C fill:#7ed321,color:#fff
    style D fill:#9013fe,color:#fff
    style E fill:#4a90e2,color:#fff
    style F fill:#f5a623,color:#fff
    style G fill:#d0021b,color:#fff
    style H fill:#7ed321,color:#fff
```

## Step-by-Step Process

### 1️⃣ Document Upload & Processing

```mermaid
graph TB
    Upload[Upload PDF Document] --> Extract[Extract Text Content]
    Extract --> Split[Split into Chunks<br/>~1000 characters each]
    Split --> Example["Example Chunks:<br/>Chunk 1: 'Polymorphism is...'<br/>Chunk 2: 'Types of inheritance...'<br/>Chunk 3: 'Java abstract classes...'"]
    
    style Upload fill:#e1f5ff
    style Extract fill:#fff4e1
    style Split fill:#f0e1ff
    style Example fill:#e1ffe1
```

### 2️⃣ Creating Searchable Embeddings

```mermaid
graph LR
    Text["Text Chunk:<br/>'Polymorphism allows...'"] --> Model[Sentence Transformer<br/>AI Model]
    Model --> Vector["Vector Embedding:<br/>[0.23, -0.41, 0.67, ..., 0.15]<br/>384 numbers"]
    Vector --> Meaning["Captures Semantic Meaning<br/>Similar concepts → Similar vectors"]
    
    style Text fill:#e1f5ff
    style Model fill:#f0e1ff
    style Vector fill:#ffe1e1
    style Meaning fill:#e1ffe1
```

### 3️⃣ Asking Questions

```mermaid
sequenceDiagram
    actor Student
    participant UI as Chat UI
    participant Search as Vector Search
    participant AI as Gemini AI
    
    Student->>UI: "What is polymorphism?"
    UI->>Search: Convert question to vector
    Search->>Search: Find most similar chunks
    
    Note over Search: Finds 5 relevant chunks<br/>from your course materials
    
    Search->>AI: Send question + relevant chunks
    AI->>AI: Generate comprehensive answer
    AI->>UI: Return detailed explanation
    UI->>Student: Display answer with sources
```

### 4️⃣ RAG Magic Explained

```mermaid
graph TD
    Q[Your Question] --> QE[Question → Vector]
    
    subgraph Documents["Your Course Materials"]
        D1[Chunk 1: OOP Concepts]
        D2[Chunk 2: Java Examples]
        D3[Chunk 3: Inheritance]
        D4[Chunk 4: Polymorphism]
        D5[Chunk 5: Abstraction]
    end
    
    QE --> Match{Find Best Matches}
    
    D1 --> Match
    D2 --> Match
    D3 --> Match
    D4 --> Match
    D5 --> Match
    
    Match -->|Relevant| C1[Chunk 4: Polymorphism ✓]
    Match -->|Relevant| C2[Chunk 3: Inheritance ✓]
    Match -->|Relevant| C3[Chunk 2: Java Examples ✓]
    
    C1 --> Prompt[Build Smart Prompt]
    C2 --> Prompt
    C3 --> Prompt
    Q --> Prompt
    
    Prompt --> AI[Gemini AI]
    AI --> Answer[📝 Comprehensive Answer]
    
    style Q fill:#4a90e2,color:#fff
    style Match fill:#f5a623,color:#fff
    style AI fill:#d0021b,color:#fff
    style Answer fill:#7ed321,color:#fff
```

## Key Benefits

### Why RAG is Better Than Just AI

```mermaid
graph TB
    subgraph Traditional["❌ Traditional AI Chatbot"]
        T1[Generic Knowledge Only] --> T2[May Give Wrong Info]
        T2 --> T3[Not Specific to Your Course]
    end
    
    subgraph RAG["✅ Learnix with RAG"]
        R1[Uses YOUR Materials] --> R2[Accurate & Relevant]
        R2 --> R3[Course-Specific Answers]
        R3 --> R4[Cites Sources]
    end
    
    style Traditional fill:#ffe1e1
    style RAG fill:#e1ffe1
```

## Technical Architecture (Simplified)

```mermaid
graph TB
    subgraph User["👤 You"]
        Browser[Web Browser]
    end
    
    subgraph Server["🖥️ Learnix Server"]
        API[FastAPI Backend]
        Embed[Embedding Model]
        Store[Vector Storage]
    end
    
    subgraph Cloud["☁️ Google Cloud"]
        Gemini[Gemini AI]
    end
    
    Browser <-->|Questions & Answers| API
    API <-->|Text → Vectors| Embed
    Embed <-->|Store & Search| Store
    API <-->|Generate Answers| Gemini
    
    style User fill:#e1f5ff
    style Server fill:#fff4e1
    style Cloud fill:#ffe1e1
```

## Example Flow

```mermaid
journey
    title Student Using Learnix
    section Setup
      Upload OOPS Notes: 5: Student
      Upload Java Notes: 5: Student
      Upload DS Notes: 5: Student
      System Processes Documents: 3: System
    section Daily Use
      Ask about Polymorphism: 5: Student
      System Searches Vectors: 4: System
      Gemini Generates Answer: 4: System
      Read Comprehensive Answer: 5: Student
    section Study Session
      Ask Follow-up Question: 5: Student
      Get Related Examples: 5: Student
      Understand Concept Better: 5: Student
```

## Performance Metrics

```mermaid
pie title Document Processing Efficiency
    "Text Extraction" : 10
    "Chunking" : 15
    "Embedding Generation" : 60
    "Vector Storage" : 15
```

```mermaid
pie title Response Time Breakdown
    "Embedding Query" : 5
    "Vector Search" : 10
    "Gemini API Call" : 75
    "Response Formatting" : 10
```

## Security & Privacy

```mermaid
graph LR
    Data[Your Documents] -->|Stored Locally| Server[Local Server]
    Server -->|API Call Only| Gemini[Gemini API]
    
    Note1[No data stored<br/>by Google] -.-> Gemini
    Note2[Documents stay<br/>on your machine] -.-> Server
    
    style Data fill:#e1ffe1
    style Server fill:#fff4e1
    style Gemini fill:#e1f5ff
```

---

## Summary

**Learnix = Your Course Materials + AI Intelligence**

1. 📚 **Upload** your PDFs
2. 🔍 **Search** with natural language
3. 🤖 **Get** comprehensive AI-generated answers
4. ✅ **Verify** with source citations

All powered by cutting-edge RAG technology that combines the best of vector search and large language models!
