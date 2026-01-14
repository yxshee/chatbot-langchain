# 🏦 RBI NBFC Chatbot - Complete Project Documentation

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture & System Design](#architecture--system-design)
3. [Technology Stack](#technology-stack)
4. [Core Components](#core-components)
5. [How It Works](#how-it-works)
6. [Project Structure](#project-structure)
7. [Setup & Installation](#setup--installation)
8. [Features & Capabilities](#features--capabilities)
9. [API Endpoints](#api-endpoints)
10. [Configuration](#configuration)
11. [Testing & Evaluation](#testing--evaluation)
12. [Deployment](#deployment)

---

## 🎯 Project Overview

### What is this project?
This is a **Retrieval-Augmented Generation (RAG) powered chatbot** that provides accurate, citation-backed answers about RBI (Reserve Bank of India) regulations for Non-Banking Financial Companies (NBFCs). It processes a 330-page RBI Master Direction document and converts it into 716 intelligent chunks for quick retrieval and response generation.

### Key Highlights
- ✅ **716 optimized document chunks** from RBI Master Direction
- ✅ **4-document retrieval** for accurate context
- ✅ **Source attribution** for all answers
- ✅ **Multiple interfaces**: Web UI, CLI, REST API
- ✅ **Production-ready** with comprehensive error handling
- ✅ **LangSmith integration** for evaluation and monitoring

### Problem It Solves
- Quickly find specific NBFC regulations without manually searching through a 330-page PDF
- Get accurate, AI-generated answers grounded in official RBI documentation
- Verify answers with source citations showing exact page numbers and excerpts
- Access regulatory information through multiple interfaces (web, CLI, API)

---

## 🏗️ Architecture & System Design

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACES                          │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌───────────┐ │
│  │ Streamlit  │  │    CLI     │  │  REST API  │  │    FAQ    │ │
│  │   Web UI   │  │ Interactive│  │  (FastAPI) │  │   Demo    │ │
│  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘  └─────┬─────┘ │
└────────┼───────────────┼───────────────┼───────────────┼────────┘
         │               │               │               │
         └───────────────┴───────────────┴───────────────┘
                                │
                      ┌─────────▼─────────┐
                      │   RAG CHAIN       │
                      │  (LangChain)      │
                      └─────────┬─────────┘
                                │
                ┌───────────────┴───────────────┐
                │                               │
         ┌──────▼──────┐              ┌────────▼────────┐
         │   RETRIEVER │              │   LLM (Gemini)  │
         │   (FAISS)   │              │   Response Gen  │
         └──────┬──────┘              └─────────────────┘
                │
         ┌──────▼──────┐
         │   VECTOR    │
         │   STORE     │
         │ (716 chunks)│
         └─────────────┘
                │
         ┌──────▼──────┐
         │  EMBEDDINGS │
         │  (Google    │
         │   text-     │
         │   embedding-│
         │    004)     │
         └─────────────┘
```

### Data Flow

```
1. USER QUERY
   ↓
2. EMBEDDING GENERATION (Query → 768-dimensional vector)
   ↓
3. VECTOR SIMILARITY SEARCH (FAISS retrieves top-k similar chunks)
   ↓
4. CONTEXT PREPARATION (Top 4 retrieved documents)
   ↓
5. LLM GENERATION (Gemini generates grounded response)
   ↓
6. RESPONSE + SOURCES (Answer with page citations)
   ↓
7. USER INTERFACE (Display formatted response)
```

### RAG Pipeline Workflow

```
┌──────────────────────────────────────────────────────────────┐
│                    DOCUMENT INGESTION                        │
│                                                              │
│  PDF File (330 pages)                                        │
│       ↓                                                      │
│  Text Extraction (PyPDF/PyMuPDF)                            │
│       ↓                                                      │
│  Text Chunking (1000 chars, 200 overlap)                    │
│       ↓                                                      │
│  Embedding Generation (768-dim vectors)                     │
│       ↓                                                      │
│  FAISS Vector Store (716 chunks indexed)                    │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                    QUERY PROCESSING                          │
│                                                              │
│  User Question                                               │
│       ↓                                                      │
│  Embed Question (768-dim vector)                            │
│       ↓                                                      │
│  Similarity Search (FAISS retrieves top-4)                  │
│       ↓                                                      │
│  Retrieve Context (4 relevant chunks)                       │
│       ↓                                                      │
│  Prompt Construction (Context + Question)                   │
│       ↓                                                      │
│  LLM Generation (Gemini 2.5 Flash)                         │
│       ↓                                                      │
│  Format Response (Answer + Citations)                       │
└──────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

### Core Technologies

#### 1. **Large Language Model (LLM)**
- **Technology**: Google Gemini 2.5 Flash
- **Purpose**: Generate natural language responses based on retrieved context
- **Configuration**: 
  - Temperature: 0.1 (factual, deterministic responses)
  - Model: `gemini-2.5-flash` (fast, cost-effective)
- **Why Gemini**: High quality, multimodal capabilities, cost-effective, reliable API

#### 2. **Embeddings**
- **Technology**: Google `text-embedding-004`
- **Purpose**: Convert text into 768-dimensional vectors for semantic search
- **Dimensions**: 768
- **Why this model**: State-of-the-art embeddings, excellent semantic understanding

#### 3. **Vector Database**
- **Technology**: FAISS (Facebook AI Similarity Search)
- **Purpose**: Efficient similarity search over 716 document chunks
- **Implementation**: `faiss-cpu` for CPU-based vector search
- **Index Type**: Flat L2 index for precise similarity matching
- **Why FAISS**: Fast, efficient, no external server required, perfect for offline use

#### 4. **Framework**
- **Technology**: LangChain 0.2.16
- **Purpose**: Orchestrate RAG pipeline, chain components together
- **Components Used**:
  - `langchain-core`: Base abstractions
  - `langchain-community`: Community integrations
  - `langchain-google-genai`: Google AI integration
- **Why LangChain**: Industry standard, modular, extensive integrations

#### 5. **PDF Processing**
- **Technologies**: 
  - PyPDF 4.3.1
  - PyMuPDF 1.24.10
- **Purpose**: Extract text from PDF documents
- **Why both**: Redundancy and better text extraction quality

#### 6. **Text Processing**
- **Technology**: TikToken 0.7.0
- **Purpose**: Token counting and text splitting
- **Why TikToken**: Accurate token counting for LLM context management

#### 7. **Web Framework**
- **Technology**: Streamlit 1.37.0+
- **Purpose**: Interactive web UI for chatbot
- **Features**: Chat interface, source display, configuration panel
- **Why Streamlit**: Rapid development, built-in chat components, easy deployment

#### 8. **API Framework**
- **Technology**: FastAPI 0.112.1 + Uvicorn 0.30.6
- **Purpose**: REST API for programmatic access
- **Features**: Asynchronous endpoints, automatic documentation
- **Why FastAPI**: Fast, modern, automatic API docs, async support

#### 9. **Monitoring & Evaluation**
- **Technology**: LangSmith 0.1.129
- **Purpose**: Track chains, evaluate responses, debug issues
- **Features**: Chain tracing, dataset evaluation, performance monitoring

#### 10. **Data Processing**
- **Technologies**:
  - Pandas 2.2.2: Data manipulation
  - NumPy 1.26.4: Numerical computing
  - Scikit-learn 1.5.1: ML utilities
- **Purpose**: Data processing, evaluation metrics

#### 11. **Development Tools**
- **Testing**: pytest 8.0.0+
- **Environment**: python-dotenv 1.0.1
- **Logging**: structlog 24.4.0
- **Web Scraping**: requests, beautifulsoup4, lxml

---

## 🧩 Core Components

### 1. **RAG Chain** (`src/rbi_nbfc_chatbot/chains/rag_chain.py`)

The heart of the application, responsible for:
- Orchestrating retrieval and generation
- Managing LLM interactions
- Formatting responses with sources

```python
Key Methods:
- build_rag_chain(): Initialize the RAG pipeline
- ask_question(): Process user queries
- _format_docs(): Format retrieved documents
```

**How it works**:
1. Takes user question as input
2. Queries the retriever for relevant chunks
3. Constructs a prompt with context + question
4. Sends to Gemini for answer generation
5. Returns formatted answer with source citations

### 2. **Retriever** (`src/rbi_nbfc_chatbot/chains/retriever.py`)

Handles vector similarity search:
- Loads FAISS index
- Performs k-nearest neighbor search
- Returns top-k relevant document chunks

```python
Key Functions:
- create_retriever(): Initialize FAISS retriever
- Retrieval configuration: k=4 (top 4 documents)
```

**How it works**:
1. Embeds user query using text-embedding-004
2. Performs cosine similarity search in FAISS index
3. Returns top 4 most similar chunks with metadata

### 3. **Document Ingestion** (`src/rbi_nbfc_chatbot/utils/ingest.py`)

Processes PDF and builds vector store:
- Loads PDF document
- Splits into chunks
- Generates embeddings
- Creates FAISS index

```python
Key Functions:
- ingest_documents(): Main ingestion pipeline
- build_vector_store(): Create FAISS index
```

**How it works**:
1. Loads PDF using PyPDF/PyMuPDF
2. Splits text into 1000-char chunks with 200 overlap
3. Generates 768-dim embeddings for each chunk
4. Stores in FAISS index (716 total chunks)

### 4. **Configuration** (`src/rbi_nbfc_chatbot/config.py`)

Centralized configuration management:
- Environment variables
- API keys
- Model settings
- File paths

```python
Key Settings:
- GEMINI_MODEL: "gemini-2.5-flash"
- RETRIEVAL_K: 4
- CHUNK_SIZE: 1000
- CHUNK_OVERLAP: 200
- TEMPERATURE: 0.1
```

### 5. **Streamlit UI** (`app.py`)

Interactive web interface:
- Chat interface
- Source visualization
- Configuration panel
- Session management

**Features**:
- Real-time chat
- Source expansion/collapse
- Export chat history
- Model parameter tuning
- Sample question buttons

### 6. **FastAPI Server** (`src/rbi_nbfc_chatbot/api/`)

REST API for programmatic access:
- `/query` endpoint for questions
- `/health` endpoint for status checks
- Automatic OpenAPI documentation

### 7. **Evaluation Suite** (`src/rbi_nbfc_chatbot/evals/`)

LangSmith-powered evaluation:
- Dataset creation
- Response evaluation
- Performance metrics
- Chain tracing

---

## 🔄 How It Works

### Complete User Journey

#### Scenario: User asks "What is a Non-Banking Financial Company?"

**Step 1: User Input**
```
User types question in Streamlit web UI:
"What is a Non-Banking Financial Company (NBFC)?"
```

**Step 2: Query Embedding**
```python
# Question is converted to 768-dim vector
embedding = GoogleGenerativeAIEmbeddings.embed_query(
    "What is a Non-Banking Financial Company (NBFC)?"
)
# Result: [0.023, -0.145, 0.089, ..., 0.234] (768 dimensions)
```

**Step 3: Vector Similarity Search**
```python
# FAISS searches 716 chunks for top-4 most similar
retriever = create_retriever(k=4)
docs = retriever.get_relevant_documents(question)

# Returns 4 most relevant chunks, e.g.:
# Chunk 143 (page 12): "A Non-Banking Financial Company (NBFC) is..."
# Chunk 287 (page 24): "NBFCs are defined under Section 45-I(f)..."
# Chunk 91 (page 8): "Classification of NBFCs includes..."
# Chunk 456 (page 38): "NBFCs must comply with..."
```

**Step 4: Context Preparation**
```python
# Retrieved chunks are formatted into context
context = """
[Source 1 - Page 12]
A Non-Banking Financial Company (NBFC) is a company registered under...

[Source 2 - Page 24]
NBFCs are defined under Section 45-I(f) of the RBI Act...

[Source 3 - Page 8]
Classification of NBFCs includes...

[Source 4 - Page 38]
NBFCs must comply with...
"""
```

**Step 5: Prompt Construction**
```python
prompt = f"""
You are an expert on RBI regulations for NBFCs. Answer the question based ONLY on the context provided.

Context:
{context}

Question: {user_question}

Provide a clear, accurate answer with specific references to the regulations.
"""
```

**Step 6: LLM Generation**
```python
# Send to Gemini 2.5 Flash
response = gemini.generate(
    prompt=prompt,
    temperature=0.1,  # Low for factual accuracy
    model="gemini-2.5-flash"
)

# Gemini generates grounded response:
"""
A Non-Banking Financial Company (NBFC) is a company registered under the 
Companies Act, 1956/2013, that is engaged in the business of loans and 
advances, acquisition of shares/stocks/bonds/securities, etc., but does not 
include any institution whose principal business is agricultural activity, 
industrial activity, purchase or sale of goods or providing services.

NBFCs are defined under Section 45-I(f) of the RBI Act, 1934...
"""
```

**Step 7: Response Formatting**
```python
formatted_response = {
    "answer": "A Non-Banking Financial Company (NBFC) is...",
    "sources": [
        {
            "content": "A Non-Banking Financial Company...",
            "page": 12,
            "source": "rbi_nbfc_master_direction.pdf"
        },
        # ... 3 more sources
    ]
}
```

**Step 8: UI Display**
```
Streamlit displays:
- Answer in chat message
- Expandable "Show 4 source excerpts" section
- Each source shows page number and relevant text
```

### Performance Characteristics

- **Query Processing Time**: 2-5 seconds
- **Embedding Generation**: ~0.5 seconds
- **Vector Search**: ~0.1 seconds (FAISS is very fast)
- **LLM Generation**: 1-4 seconds
- **Total Latency**: 2-5 seconds end-to-end

---

## 📁 Project Structure

```
chatbot-langchain/
│
├── 📄 app.py                          # Streamlit web UI (main entry point)
├── 📄 requirements.txt                # Python dependencies
├── 📄 README.md                       # Quick start guide
├── 📄 .env.example                    # Environment variable template
├── 📄 .env                           # Actual API keys (gitignored)
├── 📄 .gitignore                     # Git ignore rules
│
├── 📁 src/rbi_nbfc_chatbot/          # Main package
│   ├── 📄 __init__.py                # Package initialization
│   ├── 📄 config.py                  # Configuration management
│   │
│   ├── 📁 chains/                    # RAG pipeline components
│   │   ├── 📄 __init__.py
│   │   ├── 📄 rag_chain.py           # Main RAG chain logic
│   │   └── 📄 retriever.py           # FAISS retriever setup
│   │
│   ├── 📁 utils/                     # Utility modules
│   │   ├── 📄 __init__.py
│   │   ├── 📄 ingest.py              # Document ingestion pipeline
│   │   └── 📄 document_loader.py     # PDF loading utilities
│   │
│   ├── 📁 api/                       # FastAPI REST API
│   │   ├── 📄 __init__.py
│   │   └── 📄 main.py                # API endpoints
│   │
│   └── 📁 evals/                     # Evaluation tools
│       ├── 📄 __init__.py
│       └── 📄 langsmith_eval.py      # LangSmith evaluation
│
├── 📁 examples/                      # Demo applications
│   ├── 📄 demo_interactive.py        # CLI interactive chat
│   ├── 📄 demo_api.py                # API server demo
│   ├── 📄 demo_faq.py                # FAQ demonstration
│   └── 📄 demo_cli.py                # Simple CLI demo
│
├── 📁 scripts/                       # Utility scripts
│   ├── 📄 quick_start.py             # Quick start script
│   ├── 📄 check.py                   # System health check
│   ├── 📄 rebuild_vectorstore.py     # Rebuild FAISS index
│   ├── 📄 setup.sh                   # Setup automation
│   └── 📄 run.sh                     # Run script
│
├── 📁 tests/                         # Test suite
│   ├── 📄 test_rag_pipeline.py       # RAG pipeline tests
│   ├── 📄 test_complete_system.py    # End-to-end tests
│   └── 📄 test_document_loader.py    # Document loading tests
│
├── 📁 data/                          # Data directory
│   ├── 📁 documents/                 # Source documents
│   │   └── 📄 rbi_nbfc_master_direction.pdf  # 330-page PDF
│   │
│   └── 📁 vector_store/              # FAISS vector index
│       ├── 📄 index.faiss            # FAISS index file
│       └── 📄 index.pkl              # Metadata pickle
│
└── 📁 .venv/                         # Virtual environment (gitignored)
```

### Key Files Explained

| File | Purpose | Key Features |
|------|---------|--------------|
| `app.py` | Streamlit web UI | Chat interface, source display, config panel |
| `src/rbi_nbfc_chatbot/chains/rag_chain.py` | RAG pipeline | Orchestrates retrieval + generation |
| `src/rbi_nbfc_chatbot/chains/retriever.py` | Vector search | FAISS similarity search |
| `src/rbi_nbfc_chatbot/utils/ingest.py` | Document processing | PDF → chunks → embeddings → FAISS |
| `src/rbi_nbfc_chatbot/config.py` | Configuration | Centralized settings management |
| `src/rbi_nbfc_chatbot/api/main.py` | REST API | FastAPI endpoints for queries |
| `examples/demo_interactive.py` | CLI chat | Terminal-based Q&A |
| `scripts/quick_start.py` | Quick test | Rapid system check |
| `tests/test_complete_system.py` | Integration tests | End-to-end validation |

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.9+
- Google API Key (for Gemini)
- 4GB RAM minimum
- ~500MB disk space

### Installation Steps

#### 1. Clone Repository
```bash
git clone https://github.com/yourusername/chatbot-langchain.git
cd chatbot-langchain
```

#### 2. Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Configure Environment Variables
```bash
cp .env.example .env
# Edit .env and add your Google API key:
# GOOGLE_API_KEY=your_actual_api_key_here
```

#### 5. Verify Installation
```bash
python scripts/check.py
```

#### 6. Run Quick Start
```bash
python scripts/quick_start.py
```

### Getting API Keys

#### Google API Key (Required)
1. Visit https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy and paste into `.env` file

#### LangSmith API Key (Optional)
1. Visit https://smith.langchain.com/settings
2. Sign up/login
3. Generate API key
4. Add to `.env` file

---

## ✨ Features & Capabilities

### 1. **Multiple User Interfaces**

#### Web UI (Streamlit)
- **Launch**: `streamlit run app.py`
- **Features**:
  - Interactive chat interface
  - Real-time response streaming
  - Source citations with page numbers
  - Expandable source excerpts
  - Export chat history
  - Adjustable model parameters
  - Sample question buttons
  - Session management

#### CLI Interactive Chat
- **Launch**: `python examples/demo_interactive.py`
- **Features**:
  - Terminal-based Q&A
  - Type 'quit' to exit
  - Source display in terminal
  - Fast, lightweight

#### REST API
- **Launch**: `python examples/demo_api.py`
- **Endpoints**:
  - `POST /query`: Ask questions
  - `GET /health`: Check status
- **Features**:
  - Automatic OpenAPI docs at `/docs`
  - JSON request/response
  - Programmatic access

#### FAQ Demo
- **Launch**: `python examples/demo_faq.py`
- **Features**:
  - Pre-loaded common questions
  - Batch processing
  - Demonstration mode

### 2. **Intelligent Retrieval**

- **Top-K Search**: Retrieves 4 most relevant chunks
- **Semantic Understanding**: Understands meaning, not just keywords
- **Context Window**: 1000 characters per chunk with 200 overlap
- **Fast Search**: FAISS enables sub-second retrieval
- **Source Attribution**: Every answer cites exact pages

### 3. **Response Generation**

- **Grounded Responses**: Answers based only on retrieved context
- **Temperature Control**: 0.1 for factual accuracy
- **Citation Format**: Clear attribution to source documents
- **Error Handling**: Graceful degradation on failures
- **Streaming Support**: Real-time response generation

### 4. **Configuration & Customization**

- **Model Selection**: Switch between Gemini models
- **Temperature Adjustment**: Control creativity vs. accuracy
- **Retrieval Tuning**: Adjust number of retrieved documents
- **Source Toggle**: Enable/disable source display
- **Chain Rebuild**: Force fresh initialization

### 5. **Monitoring & Evaluation**

- **LangSmith Integration**: Track all chain executions
- **Performance Metrics**: Response time, token usage
- **Dataset Evaluation**: Test against known Q&A pairs
- **Debug Tracing**: Inspect retrieval and generation steps

---

## 🌐 API Endpoints

### POST /query

Ask a question to the chatbot.

**Request:**
```json
{
  "question": "What is a Non-Banking Financial Company?",
  "return_sources": true
}
```

**Response:**
```json
{
  "answer": "A Non-Banking Financial Company (NBFC) is a company...",
  "sources": [
    {
      "content": "Full text of retrieved chunk...",
      "page": 12,
      "source": "rbi_nbfc_master_direction.pdf"
    }
  ],
  "metadata": {
    "model": "gemini-2.5-flash",
    "retrieval_k": 4,
    "response_time_seconds": 2.34
  }
}
```

### GET /health

Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "model": "gemini-2.5-flash",
  "vector_store_loaded": true,
  "document_count": 716
}
```

---

## ⚙️ Configuration

### Environment Variables (.env)

```env
# Required
GOOGLE_API_KEY=your_google_api_key_here

# Optional
LANGSMITH_API_KEY=your_langsmith_key
GEMINI_MODEL=gemini-2.5-flash
GOOGLE_EMBEDDING_MODEL=models/text-embedding-004
TEMPERATURE=0.1
RETRIEVAL_K=4
```

### Model Configuration

| Parameter | Default | Description | Range |
|-----------|---------|-------------|-------|
| `GEMINI_MODEL` | `gemini-2.5-flash` | LLM model name | Any Gemini model |
| `TEMPERATURE` | `0.1` | Response creativity | 0.0 - 1.0 |
| `RETRIEVAL_K` | `4` | Number of chunks to retrieve | 1 - 10 |
| `CHUNK_SIZE` | `1000` | Characters per chunk | 500 - 2000 |
| `CHUNK_OVERLAP` | `200` | Overlap between chunks | 0 - 500 |

### File Paths

```python
PROJECT_ROOT/
├── data/
│   ├── documents/
│   │   └── rbi_nbfc_master_direction.pdf
│   └── vector_store/
│       ├── index.faiss
│       └── index.pkl
```

---

## 🧪 Testing & Evaluation

### Test Suite

#### 1. Quick System Check
```bash
python scripts/check.py
```
Verifies:
- API keys present
- Dependencies installed
- Vector store exists
- Model accessibility

#### 2. Complete System Test
```bash
python tests/test_complete_system.py
```
Tests:
- Document loading
- Embedding generation
- FAISS retrieval
- RAG chain execution
- Response formatting

#### 3. RAG Pipeline Test
```bash
python tests/test_rag_pipeline.py
```
Tests:
- Retriever initialization
- Query processing
- Context retrieval
- Answer generation

#### 4. LangSmith Evaluation
```bash
python -m src.rbi_nbfc_chatbot.evals.langsmith_eval
```
Evaluates:
- Answer accuracy
- Source relevance
- Response quality
- Latency metrics

### Running with Pytest

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_rag_pipeline.py

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=src/rbi_nbfc_chatbot
```

---

## 🚢 Deployment

### Local Deployment

#### Streamlit Web UI
```bash
streamlit run app.py
# Access at http://localhost:8501
```

#### FastAPI Server
```bash
python examples/demo_api.py
# API at http://localhost:8000
# Docs at http://localhost:8000/docs
```

### Production Deployment Options

#### 1. Streamlit Cloud
```bash
# Push to GitHub
git push origin main

# Deploy on Streamlit Cloud
# 1. Visit share.streamlit.io
# 2. Connect GitHub repo
# 3. Add secrets (API keys)
# 4. Deploy
```

#### 2. Docker Container
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["streamlit", "run", "app.py", "--server.port=8501"]
```

#### 3. Cloud Platforms
- **Google Cloud Run**: Containerized FastAPI/Streamlit
- **AWS EC2**: Full VM deployment
- **Heroku**: Easy deployment with buildpacks
- **Azure App Service**: Managed app hosting

### Performance Considerations

- **Memory**: ~4GB recommended for FAISS index
- **CPU**: 2+ cores for concurrent requests
- **Storage**: ~500MB for vector store + dependencies
- **Network**: Google API access required

### Security Best Practices

1. **Never commit API keys**: Use `.env` files (gitignored)
2. **Rotate keys regularly**: Generate new API keys periodically
3. **Use environment secrets**: In production, use secret managers
4. **Rate limiting**: Implement rate limits on API endpoints
5. **Input validation**: Sanitize user inputs
6. **HTTPS only**: Use SSL/TLS in production

---

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| **Total Documents** | 716 chunks |
| **Embedding Dimensions** | 768 |
| **Average Query Time** | 2-5 seconds |
| **Retrieval Accuracy** | ~85% relevant |
| **Memory Usage** | ~4GB |
| **Index Load Time** | ~1 second |
| **Vector Search Time** | <100ms |

---

## 🔧 Troubleshooting

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| **API Key Error** | Add `GOOGLE_API_KEY` to `.env` file |
| **FAISS Not Found** | Run `python -m src.rbi_nbfc_chatbot.utils.ingest` |
| **Import Errors** | Run `pip install -r requirements.txt` |
| **Model Error** | Check model name in `.env` (use `gemini-2.5-flash`) |
| **Slow Responses** | Reduce `RETRIEVAL_K` or upgrade to faster model |
| **Memory Error** | Close other applications or upgrade RAM |

### Debug Mode

```bash
# Enable verbose logging
export LOG_LEVEL=DEBUG

# Run with tracing
LANGSMITH_TRACING_V2=true python app.py
```

---

## 🎓 Learning Resources

### Understanding RAG
- LangChain RAG documentation
- FAISS similarity search guide
- Google Gemini API docs

### Code Components
- `chains/rag_chain.py`: Study RAG implementation
- `utils/ingest.py`: Learn document processing
- `app.py`: Explore Streamlit patterns

### Further Enhancements
1. Add conversation memory
2. Implement query rewriting
3. Add hybrid search (keyword + semantic)
4. Create feedback loop
5. Multi-document support

---

## 📝 Summary

This RBI NBFC Chatbot is a complete RAG-powered application that demonstrates:

✅ **Modern AI Architecture**: LLM + Vector DB + Embeddings  
✅ **Production-Ready**: Error handling, testing, monitoring  
✅ **Multiple Interfaces**: Web, CLI, API  
✅ **Best Practices**: Configuration management, modular design  
✅ **Documentation**: Comprehensive guides and examples  

**Built with**: Google Gemini, LangChain, FAISS, Streamlit, FastAPI

**Key Achievement**: Transforms a 330-page PDF into an intelligent, conversational assistant with source attribution.

---

*Last Updated: January 2026*
*Version: 2.0.0*
