# 🏗️ Project Structure - RBI NBFC Chatbot

This document explains the professional project organization and how each component works together.

## 📁 Directory Structure

```
proj2/
├── .env                          # Environment variables (API keys, configuration)
├── .gitignore                    # Git ignore patterns
├── README.md                     # Main project documentation
├── requirements.txt              # Python dependencies
│
├── data/                         # Data files
│   ├── documents/                # Source documents
│   │   └── rbi_nbfc_master_direction.pdf  # 330-page RBI Master Direction
│   └── vector_store/             # Vector database
│       └── index.faiss/          # FAISS vector store (716 chunks)
│
├── docs/                         # Documentation
│   ├── QUICKSTART.md             # Quick start guide
│   ├── VIDEO_GUIDE.md            # Video demonstration guide
│   └── STRUCTURE.md              # This file - project structure documentation
│
├── examples/                     # Demonstration scripts
│   ├── demo_api.py               # FastAPI web server
│   ├── demo_cli.py               # CLI retrieval demonstration
│   ├── demo_faq.py               # FAQ demonstration (10 questions)
│   └── demo_interactive.py       # Interactive chatbot session
│
├── scripts/                      # Utility scripts
│   ├── check.py                  # Project status checker
│   ├── run.sh                    # Run script
│   └── setup.sh                  # Setup script
│
├── src/                          # Source code (main package)
│   └── rbi_nbfc_chatbot/         # Main Python package
│       ├── __init__.py           # Package initialization and exports
│       ├── config.py             # Centralized configuration
│       │
│       ├── chains/               # RAG chain components
│       │   ├── __init__.py
│       │   ├── rag_chain.py      # Main RAG chain implementation
│       │   └── retriever.py      # Document retriever (FAISS)
│       │
│       ├── utils/                # Utility functions
│       │   ├── __init__.py
│       │   ├── document_loader.py  # PDF loading and chunking
│       │   └── ingest.py         # Document ingestion pipeline
│       │
│       ├── api/                  # Web API
│       │   ├── __init__.py
│       │   └── server.py         # FastAPI server implementation
│       │
│       └── evals/                # Evaluation framework
│           ├── __init__.py
│           └── langsmith_eval.py # LangSmith evaluation integration
│
└── tests/                        # Test files
    ├── __init__.py
    └── test_rag_pipeline.py      # RAG pipeline tests
```

## 🔧 Core Components

### 1. Configuration (`src/rbi_nbfc_chatbot/config.py`)

**Purpose**: Centralized configuration management

**Key Features**:
- Environment variable loading
- Path management (PROJECT_ROOT, data directories)
- Model configuration (Gemini, embeddings)
- API settings (host, port)
- Retrieval parameters (k, chunk size)

**Usage**:
```python
from src.rbi_nbfc_chatbot.config import (
    GEMINI_MODEL,
    VECTOR_STORE_PATH,
    RETRIEVAL_K
)
```

### 2. Document Retriever (`src/rbi_nbfc_chatbot/chains/retriever.py`)

**Purpose**: FAISS-based document retrieval

**Key Features**:
- Loads FAISS vector store
- Creates Google Gemini embeddings
- Retrieves top-k relevant documents
- Configurable retrieval parameters

**Functions**:
- `create_retriever()`: Initialize FAISS retriever
- `get_relevant_documents()`: Search for relevant docs

**Usage**:
```python
from src.rbi_nbfc_chatbot.chains import create_retriever

retriever = create_retriever()
docs = retriever.get_relevant_documents("What is an NBFC?")
```

### 3. RAG Chain (`src/rbi_nbfc_chatbot/chains/rag_chain.py`)

**Purpose**: Complete Retrieval-Augmented Generation pipeline

**Key Features**:
- Combines LLM + retriever + prompt
- Answer generation with source attribution
- Google Gemini 2.5 Flash integration
- Configurable prompt template

**Classes**:
- `RAGChain`: Main RAG pipeline class
  - `ask_question()`: Ask with full response (answer + sources)
  - `ask()`: Ask and get just the answer text

**Functions**:
- `build_rag_chain()`: Factory function to create RAG chain

**Usage**:
```python
from src.rbi_nbfc_chatbot.chains import build_rag_chain

rag_chain = build_rag_chain()
response = rag_chain.ask_question("What are capital requirements?")
print(response["answer"])
print(response["sources"])
```

### 4. Document Ingestion (`src/rbi_nbfc_chatbot/utils/`)

**Purpose**: PDF processing and vector store creation

**Key Components**:

**document_loader.py**:
- `load_pdf()`: Load PDF using PyPDFLoader
- `split_documents()`: Chunk documents (RecursiveCharacterTextSplitter)

**ingest.py**:
- `build_vector_store()`: Create FAISS index from documents
- `ingest_documents()`: Complete ingestion pipeline
  - Load PDF → Split → Embed → Save FAISS index

**Usage**:
```python
from src.rbi_nbfc_chatbot.utils import ingest_documents

# Run full ingestion
ingest_documents(force=True)
```

**Command line**:
```bash
python -m src.rbi_nbfc_chatbot.utils.ingest
```

### 5. FastAPI Server (`src/rbi_nbfc_chatbot/api/server.py`)

**Purpose**: REST API for chatbot queries

**Key Features**:
- FastAPI with automatic OpenAPI docs
- CORS middleware enabled
- Lazy loading of RAG chain
- JSON request/response
- Error handling

**Endpoints**:
- `GET /`: API information
- `GET /health`: Health check
- `POST /ask`: Ask a question
- `GET /docs`: Swagger UI
- `GET /redoc`: ReDoc documentation

**Usage**:
```bash
python examples/demo_api.py
# Visit: http://localhost:8000/docs
```

**API Request**:
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is an NBFC?", "max_sources": 4}'
```

### 6. Evaluation (`src/rbi_nbfc_chatbot/evals/langsmith_eval.py`)

**Purpose**: LangSmith-based evaluation framework

**Key Features**:
- Dataset-based evaluation
- Automatic metric calculation
- Experiment tracking
- Integration with LangSmith platform

**Functions**:
- `run_evaluation()`: Run eval on LangSmith dataset

**Usage**:
```python
from src.rbi_nbfc_chatbot.evals import run_evaluation

results = run_evaluation("rbi-nbfc-faq", "experiment-1")
```

## 🎮 Usage Examples

### Example 1: Simple Question Answering

```python
from src.rbi_nbfc_chatbot import build_rag_chain

# Build RAG chain
rag = build_rag_chain()

# Ask a question
response = rag.ask_question("What is the minimum NOF for NBFCs?")

print("Answer:", response["answer"])
print("Sources:", len(response["sources"]), "documents")
```

### Example 2: Custom Configuration

```python
from src.rbi_nbfc_chatbot import build_rag_chain

# Build with custom settings
rag = build_rag_chain(
    model_name="gemini-2.5-flash",
    temperature=0.2,
    k=5  # Retrieve 5 documents instead of 4
)

answer = rag.ask("Explain NBFC deposit regulations")
print(answer)
```

### Example 3: Using the Retriever Directly

```python
from src.rbi_nbfc_chatbot import create_retriever

# Create retriever
retriever = create_retriever(k=3)

# Get relevant documents
docs = retriever.get_relevant_documents("NBFC licensing requirements")

for i, doc in enumerate(docs, 1):
    print(f"\nDocument {i}:")
    print(doc.page_content[:200])
    print(f"Page: {doc.metadata.get('page')}")
```

### Example 4: Running the API Server

```python
# examples/demo_api.py
from src.rbi_nbfc_chatbot.api import app
import uvicorn

uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 🔄 Data Flow

```
1. User Question
   ↓
2. RAG Chain receives question
   ↓
3. Question → Embeddings (Google text-embedding-004)
   ↓
4. Embeddings → FAISS Vector Store
   ↓
5. FAISS returns top-k relevant documents (k=4)
   ↓
6. Documents + Question → Prompt Template
   ↓
7. Prompt → Google Gemini 2.5 Flash
   ↓
8. LLM generates answer
   ↓
9. Answer + Source Documents → User
```

## 📦 Dependencies

### Core Dependencies
- **langchain** (0.2.16): RAG framework
- **langchain-google-genai**: Google Gemini integration
- **langchain-community**: Community integrations (FAISS, loaders)
- **faiss-cpu**: Vector similarity search
- **pypdf**: PDF processing

### API Dependencies
- **fastapi**: Web framework
- **uvicorn**: ASGI server
- **pydantic**: Data validation

### Utilities
- **python-dotenv**: Environment variable management
- **langsmith**: Evaluation platform

## 🚀 Quick Start Commands

```bash
# 1. Setup
source .venv/bin/activate
pip install -r requirements.txt

# 2. Check status
python scripts/check.py

# 3. Run demos
python examples/demo_cli.py          # CLI demo
python examples/demo_faq.py          # FAQ demo
python examples/demo_interactive.py  # Interactive chat
python examples/demo_api.py          # Web API

# 4. Run tests
python tests/test_rag_pipeline.py

# 5. Ingest new documents (if needed)
python -m src.rbi_nbfc_chatbot.utils.ingest
```

## 🎯 Design Principles

### 1. **Modularity**
- Each component has a single responsibility
- Clean imports and exports via `__init__.py`
- Minimal coupling between modules

### 2. **Configuration**
- Centralized configuration in `config.py`
- Environment variables for sensitive data
- Sensible defaults for all parameters

### 3. **Documentation**
- Comprehensive docstrings
- Type hints throughout
- Usage examples in docstrings

### 4. **Error Handling**
- Graceful error messages
- File existence checks
- API key validation

### 5. **Professional Structure**
- Standard Python package layout
- Clear separation: src/, examples/, tests/, docs/
- Follows PEP 8 conventions

## 📝 Key Files Explained

### `.env`
Environment variables for API keys and configuration.

### `requirements.txt`
Python package dependencies with pinned versions.

### `src/rbi_nbfc_chatbot/__init__.py`
Package entry point - exports all public APIs.

### `scripts/check.py`
Comprehensive project status checker:
- Validates environment configuration
- Checks file existence
- Tests dependencies
- Provides actionable feedback

## 🎨 Import Patterns

```python
# Import the RAG chain
from src.rbi_nbfc_chatbot import build_rag_chain, RAGChain

# Import retriever
from src.rbi_nbfc_chatbot import create_retriever

# Import utilities
from src.rbi_nbfc_chatbot import ingest_documents

# Import configuration
from src.rbi_nbfc_chatbot import (
    GEMINI_MODEL,
    VECTOR_STORE_PATH
)

# Import API
from src.rbi_nbfc_chatbot.api import app

# Import evaluation
from src.rbi_nbfc_chatbot.evals import run_evaluation
```

## 🔧 Extension Points

### Adding New Prompts
Edit `src/rbi_nbfc_chatbot/chains/rag_chain.py` - modify `DEFAULT_PROMPT_TEMPLATE`

### Adding New API Endpoints
Edit `src/rbi_nbfc_chatbot/api/server.py` - add new FastAPI routes

### Adding New Evaluation Metrics
Edit `src/rbi_nbfc_chatbot/evals/langsmith_eval.py` - add custom evaluators

### Changing Vector Store
Edit `src/rbi_nbfc_chatbot/chains/retriever.py` - replace FAISS with alternatives

## 🏆 Best Practices

1. **Always use the config module** for paths and settings
2. **Don't hardcode paths** - use config constants
3. **Add docstrings** to all functions and classes
4. **Use type hints** for better IDE support
5. **Test changes** with `scripts/check.py`
6. **Update documentation** when adding features

## 📚 Related Documentation

- **README.md**: Main project documentation
- **docs/QUICKSTART.md**: Quick start guide
- **docs/VIDEO_GUIDE.md**: Video demonstration guide
- **API Docs**: http://localhost:8000/docs (when server running)

---

**Last Updated**: 2025-04-23  
**Version**: 2.0.0  
**Maintainer**: RBI NBFC Chatbot Team
