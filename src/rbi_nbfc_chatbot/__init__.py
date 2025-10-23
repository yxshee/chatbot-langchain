"""RBI NBFC Chatbot Package.

A Retrieval-Augmented Generation (RAG) chatbot for answering questions
about RBI (Reserve Bank of India) NBFC (Non-Banking Financial Company) regulations.

This package provides:
- RAG chain for question answering
- Document retrieval from FAISS vector store
- FastAPI web server
- Document ingestion utilities
- LangSmith evaluation tools
"""

__version__ = "2.0.0"

# Core components
from .api import app
from .chains import RAGChain, build_rag_chain, create_retriever
from .config import EMBEDDING_MODEL, GEMINI_MODEL, PDF_PATH, VECTOR_STORE_PATH
from .utils import build_vector_store, ingest_documents

__all__ = [
    # RAG components
    "build_rag_chain",
    "RAGChain",
    "create_retriever",
    # API
    "app",
    # Utilities
    "ingest_documents",
    "build_vector_store",
    # Configuration
    "GEMINI_MODEL",
    "EMBEDDING_MODEL",
    "VECTOR_STORE_PATH",
    "PDF_PATH",
]
