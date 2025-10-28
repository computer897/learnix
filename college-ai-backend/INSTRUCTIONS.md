# 🎓 Learnix - AI Study Assistant

**Learnix** is an intelligent RAG (Retrieval-Augmented Generation) chatbot designed for students. Upload your textbooks, lecture notes, and study materials, then ask questions to get AI-powered answers directly from your documents!

---

## ✨ Features

- 📚 **Multi-Format Support**: Upload PDF, DOCX, and TXT files
- 🔍 **Smart Search**: Semantic vector search finds relevant content
- 🤖 **AI-Powered**: Google Gemini generates comprehensive answers
- ✂️ **Auto-Chunking**: Splits large documents for better retrieval
- 💾 **Persistent Storage**: Documents saved and auto-loaded on restart
- 🚫 **Duplicate Detection**: Prevents re-uploading same files
- 🎨 **Modern UI**: Clean chat interface with dark/light theme
- ⚡ **Fast**: Optimized for quick responses

---

## 🚀 Quick Start Guide

### Prerequisites

- **Python 3.9+** installed on your system
- **Google Gemini API Key** (get free from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Step 1: Setup Virtual Environment

```powershell
# Navigate to project directory
cd D:\learnix\college-ai-backend

# Create virtual environment (if not exists)
python -m venv D:\learnix\.venv

# Activate virtual environment
D:\learnix\.venv\Scripts\Activate.ps1
```

**Note**: If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 2: Install Dependencies

```powershell
pip install -r requirements.txt
```

This installs:
- FastAPI, Uvicorn (web server)
- Sentence-Transformers (embeddings)
- PyPDF2, python-docx (document processing)
- Google Generative AI (Gemini API)
- And other required packages

### Step 3: Configure Environment

Create a `.env` file in the project root:

```env
# Production mode (set to 1 for mock mode without API)
USE_MOCKS=0

# Get your free API key from https://makersuite.google.com/app/apikey
GEMINI_API_KEY=your_api_key_here
```

### Step 4: Run the Server

**Option A - Simple Method:**
```powershell
cd D:\learnix\college-ai-backend
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

**Option B - With Full Path:**
```powershell
Push-Location D:\learnix\college-ai-backend
D:\learnix\.venv\Scripts\python.exe -m uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

**Option C - Direct Python:**
```powershell
cd D:\learnix\college-ai-backend
python -m uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

### Step 5: Access the Application

Once you see:
```
✅ Loaded X documents (Y chunks) into the index
INFO: Application startup complete.
```

Open your browser and visit:
- **Chat Interface**: http://127.0.0.1:8000
- **API Documentation**: http://127.0.0.1:8000/docs

---

## 📖 How to Use

### 1️⃣ Upload Documents

1. Click the **📎 Upload** button in the chat interface
2. Select your study materials (PDF, DOCX, or TXT)
3. Wait for the success message
4. Your documents are now indexed and searchable!

**Supported Files:**
- `.pdf` - Textbooks, lecture slides, papers
- `.docx` - Word documents, assignments
- `.txt` - Notes, code files

### 2️⃣ Ask Questions

Type your question in the chat input. Examples:

**Programming Questions:**
- "What is polymorphism in Java?"
- "Explain method overloading vs overriding"
- "How do interfaces work in Java?"

**Data Structures:**
- "Explain binary search trees"
- "What is the time complexity of quicksort?"
- "Compare arrays and linked lists"

**OOP Concepts:**
- "What are the 4 pillars of OOP?"
- "Explain encapsulation with examples"
- "What is inheritance?"

### 3️⃣ Get AI-Powered Answers

The system will:
1. 🔍 Search through your uploaded documents
2. 📝 Find the 10 most relevant text chunks
3. 🤖 Use Gemini AI to generate a comprehensive answer
4. ✅ Present it in student-friendly format

---

## 🛠️ Project Structure

```
college-ai-backend/
│
├── app.py                      # Main FastAPI application
├── requirements.txt            # Python dependencies
├── .env                        # Environment config (create this!)
├── .env.example               # Environment template
├── README.md                  # Documentation
├── test_models.py             # Test Gemini connection
│
├── utils/                     # Core modules
│   ├── __init__.py
│   ├── embeddings.py          # Generate embeddings
│   ├── rag.py                 # Vector search index
│   ├── gemini.py              # Gemini API client
│   ├── loader.py              # Extract text from files
│   ├── storage.py             # Persistent storage
│   └── chunker.py             # Split documents into chunks
│
├── frontend/                  # Web interface
│   ├── index.html             # Chat UI
│   ├── styles.css             # Styling
│   └── app.js                 # Frontend logic
│
├── data/                      # Uploaded files (auto-created)
│   ├── *.pdf                  # Original documents
│   ├── *.txt                  # Extracted text
│   └── documents_metadata.json # Document info
│
└── storage/                   # Metadata storage (auto-created)
```

---

## 🔧 Configuration

### Environment Variables (`.env`)

```env
# Mode Selection
USE_MOCKS=0          # 0 = Production (Gemini API), 1 = Mock mode

# API Keys
GEMINI_API_KEY=your_key_here    # Get from Google AI Studio
```

### Chunking Settings (`utils/chunker.py`)

```python
chunk_size = 1000    # Characters per chunk
overlap = 200        # Character overlap between chunks
```

### Retrieval Settings (`app.py`)

```python
top_k = 10          # Number of chunks to retrieve per query
```

---

## 🐛 Troubleshooting

### ❌ "ModuleNotFoundError"

**Solution:**
```powershell
pip install -r requirements.txt
```

### ❌ "Port 8000 already in use"

**Solution:** Use a different port
```powershell
uvicorn app:app --reload --host 127.0.0.1 --port 8001
```

### ❌ "No text extracted from file"

**Causes:**
- PDF is scanned (image-only, not text-based)
- File is corrupted
- Unsupported format

**Solution:** Convert scanned PDFs to text-based PDFs using OCR tools

### ❌ "I don't have enough information"

**Causes:**
- No documents uploaded yet
- Documents still loading (check terminal)
- Question not related to uploaded content

**Solution:**
1. Upload relevant documents
2. Wait for "✅ Loaded X documents" message
3. Ask questions related to your uploaded materials

### ❌ "Error calling Gemini API"

**Causes:**
- Invalid API key
- Rate limit exceeded
- Network issues

**Solution:**
```powershell
# Test your API key
python test_models.py

# Check .env file
GEMINI_API_KEY=your_actual_key_here
```

---

## 📡 API Endpoints

### Health Check
```http
GET /api/health

Response:
{
  "status": "ok",
  "mode": "production"
}
```

### Upload Document
```http
POST /api/upload/
Content-Type: multipart/form-data

Body:
  - file: [your file]

Response:
{
  "message": "filename.pdf uploaded successfully",
  "filename": "filename.pdf",
  "status": "new",
  "doc_hash": "abc123..."
}
```

### Ask Question
```http
POST /api/ask/
Content-Type: application/x-www-form-urlencoded

Body:
  - question: "What is polymorphism?"
  - top_k: 10

Response:
{
  "answer": "Polymorphism is...",
  "sources": ["chunk_1", "chunk_2", ...]
}
```

### List Documents
```http
GET /api/documents/

Response:
{
  "documents": [
    {
      "filename": "java_book.pdf",
      "size": 1234567,
      "uploaded_at": "2025-10-27T10:30:00"
    }
  ]
}
```

---

## 🎯 Tips for Best Results

1. ✅ **Upload Quality Documents**: Use text-based PDFs, not scanned images
2. ✅ **Be Specific**: Ask clear, focused questions
3. ✅ **Upload Related Materials**: More relevant docs = better answers
4. ✅ **Wait for Loading**: Let all chunks index before querying
5. ✅ **Use Keywords**: Include key terms from your documents

---

## 🔒 Security & Privacy

- 🔐 Keep your `.env` file private (never commit to Git)
- 🚫 Add `.env` to `.gitignore`
- 🔑 Don't share your Gemini API key
- 💾 Documents are stored locally in the `data/` folder

---

## 📊 System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| Python | 3.9 | 3.11+ |
| RAM | 4 GB | 8 GB |
| Storage | 500 MB + docs | 2 GB + docs |
| Internet | Required for API | Required for API |

---

## 🆘 Need Help?

**Check These First:**
1. 📋 Terminal output for error messages
2. ✅ All dependencies installed (`pip list`)
3. 🔑 `.env` file configured correctly
4. 🌐 Internet connection active
5. 📖 This README for troubleshooting

**Test Your Setup:**
```powershell
# Test Gemini API connection
python test_models.py

# Check Python version
python --version

# List installed packages
pip list
```

---

## 🎓 Example Usage

```
You: What is polymorphism in Java?

Learnix: Polymorphism is one of the fundamental principles of 
object-oriented programming that allows objects to take many forms. 
In Java, it enables you to write flexible and reusable code by 
allowing a single interface to represent different underlying types.

There are two main types of polymorphism in Java:

1. Compile-time Polymorphism (Method Overloading): This occurs when 
multiple methods have the same name but different parameters. The 
compiler determines which method to call based on the method signature.

2. Runtime Polymorphism (Method Overriding): This happens when a 
subclass provides a specific implementation of a method already 
defined in its parent class. The decision of which method to execute 
is made at runtime based on the actual object type...
```

---

## 📝 Development Notes

**Auto-Reload Mode:**
```powershell
uvicorn app:app --reload
```
Server automatically restarts when code changes are detected.

**Mock Mode (No API Required):**
```env
USE_MOCKS=1
```
Returns document excerpts without AI generation - useful for testing.

---

## 🙏 Credits

Built with:
- **FastAPI** - Modern Python web framework
- **Google Gemini** - AI language model
- **Sentence Transformers** - Semantic embeddings
- **PyPDF2** - PDF text extraction
- **python-docx** - Word document processing

---

## 📄 License

This project is for educational purposes.

---

<div align="center">

**🎓 Happy Learning with Learnix! 📚**

*Transform your study materials into an interactive AI tutor*

</div>
