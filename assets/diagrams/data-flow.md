# Learnix Data Flow Diagrams

## RAG (Retrieval-Augmented Generation) Process

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant API as FastAPI Backend
    participant Embedder as Embedding Model
    participant Index as Vector Index
    participant Gemini as Gemini API
    
    User->>Frontend: Types question
    Frontend->>API: POST /api/ask
    
    Note over API: Receive user question
    API->>Embedder: Embed question text
    Embedder->>Embedder: Generate 384-dim vector
    Embedder-->>API: Question embedding
    
    API->>Index: Search with query vector
    Index->>Index: Cosine similarity search
    Index->>Index: Rank by relevance
    Index-->>API: Top-5 relevant chunks
    
    Note over API: Build enhanced prompt
    API->>API: Combine question + context
    API->>Gemini: Send prompt with context
    
    Gemini->>Gemini: Generate comprehensive answer
    Gemini-->>API: Generated response
    
    API-->>Frontend: Return answer + sources
    Frontend-->>User: Display answer
```

## Document Ingestion Flow

```mermaid
flowchart TD
    Start([User Uploads PDF]) --> Validate{Valid PDF?}
    Validate -->|No| Error[Return Error Message]
    Validate -->|Yes| Extract[Extract Text from PDF<br/>PyPDF2]
    
    Extract --> Chunk[Split into Chunks<br/>1000 chars, 200 overlap]
    Chunk --> Count{Count Chunks}
    
    Count --> Loop[For Each Chunk]
    Loop --> Embed[Generate Embedding<br/>384-dim vector]
    Embed --> Store[Store in Index<br/>chunk_id + embedding]
    
    Store --> More{More Chunks?}
    More -->|Yes| Loop
    More -->|No| Complete[Document Indexed<br/>Ready for Search]
    
    Complete --> Success([Return Success])
    Error --> End([End])
    Success --> End
    
    style Start fill:#4a90e2
    style Success fill:#7ed321
    style Error fill:#d0021b
    style Complete fill:#f5a623
```

## Question Answering Flow

```mermaid
flowchart LR
    Q[User Question] --> E1[Embed Question]
    E1 --> S[Similarity Search]
    
    subgraph VectorDB[Vector Index]
        S --> R1[Chunk 1<br/>Score: 0.95]
        S --> R2[Chunk 2<br/>Score: 0.89]
        S --> R3[Chunk 3<br/>Score: 0.85]
        S --> R4[Chunk 4<br/>Score: 0.82]
        S --> R5[Chunk 5<br/>Score: 0.78]
    end
    
    R1 --> C[Combine Context]
    R2 --> C
    R3 --> C
    R4 --> C
    R5 --> C
    
    C --> P[Build Prompt]
    Q --> P
    
    P --> G[Gemini API]
    G --> A[Generated Answer]
    
    A --> F[Format Response]
    F --> U[Display to User]
    
    style Q fill:#e1f5ff
    style VectorDB fill:#e1ffe1
    style G fill:#ffe1e1
    style U fill:#f0e1ff
```

## Embedding Generation Process

```mermaid
graph TD
    Input[Input Text] --> Tokenize[Tokenize<br/>WordPiece Tokenizer]
    Tokenize --> BERT[BERT-based Encoder<br/>6 layers, 384 hidden]
    
    BERT --> Pool[Mean Pooling<br/>Average token embeddings]
    Pool --> Norm[L2 Normalization<br/>Unit vector]
    
    Norm --> Vector[384-dim Vector<br/>[-0.5, 0.2, 0.8, ...]]
    
    Vector --> Compare{Purpose}
    Compare -->|Storage| DB[(Vector Index)]
    Compare -->|Search| Sim[Cosine Similarity]
    
    style Input fill:#e1f5ff
    style BERT fill:#f0e1ff
    style Vector fill:#ffe1e1
    style DB fill:#e1ffe1
```

## Complete Request-Response Cycle

```mermaid
stateDiagram-v2
    [*] --> UserInput: User asks question
    
    UserInput --> EmbedQuestion: Embed query
    EmbedQuestion --> SearchVectors: Search index
    
    SearchVectors --> RetrieveContext: Get top-K chunks
    RetrieveContext --> BuildPrompt: Combine Q + Context
    
    BuildPrompt --> CallGemini: Send to Gemini API
    CallGemini --> GenerateAnswer: LLM processes
    
    GenerateAnswer --> FormatResponse: Format & validate
    FormatResponse --> ReturnToUser: Send response
    
    ReturnToUser --> [*]: Display answer
    
    note right of SearchVectors
        Cosine similarity
        Top-5 results
        Threshold: 0.7
    end note
    
    note right of CallGemini
        Model: gemini-1.5-flash
        Temperature: 0.7
        Max tokens: 2048
    end note
```

## System State Transitions

```mermaid
stateDiagram-v2
    [*] --> Startup: Server starts
    Startup --> LoadingModel: Load embedding model
    LoadingModel --> LoadingDocs: Load existing documents
    
    LoadingDocs --> Ready: All documents indexed
    
    Ready --> Processing: Receive request
    Processing --> Embedding: Generate embedding
    Embedding --> Searching: Search index
    Searching --> Generating: Call Gemini
    Generating --> Ready: Return response
    
    Ready --> Uploading: New document upload
    Uploading --> Extracting: Extract text
    Extracting --> Chunking: Split into chunks
    Chunking --> Indexing: Embed & store
    Indexing --> Ready: Document added
    
    Ready --> [*]: Server shutdown
```
