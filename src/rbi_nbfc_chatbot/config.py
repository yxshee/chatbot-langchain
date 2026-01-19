"""Configuration module for RBI NBFC Chatbot."""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ---------------------------------------------------------------------------
# Provider
# ---------------------------------------------------------------------------
# This repository ships with a prebuilt FAISS index under `data/vector_store/`
# created using Google Gemini embeddings (`models/text-embedding-004`, 768-d).
#
# To keep the project simple and consistently runnable, this codebase uses
# Google Gemini only.

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
DOCUMENTS_DIR = DATA_DIR / "documents"
VECTOR_STORE_DIR = DATA_DIR / "vector_store"

# Ensure directories exist
DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)

# PDF file path
PDF_PATH = DOCUMENTS_DIR / "rbi_nbfc_master_direction.pdf"

# FAISS index path
FAISS_INDEX_PATH = VECTOR_STORE_DIR / "index.faiss"

# API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")

# Model configuration
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
GOOGLE_EMBEDDING_MODEL = os.getenv("GOOGLE_EMBEDDING_MODEL", "models/text-embedding-004")

# Shared
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.1"))

# Backwards-compatible alias used across the codebase/tests.
EMBEDDING_MODEL = GOOGLE_EMBEDDING_MODEL

# Retriever configuration
RETRIEVAL_K = int(os.getenv("RETRIEVAL_K", "4"))

# Path strings (for compatibility)
VECTOR_STORE_PATH = str(FAISS_INDEX_PATH)

# Chunking configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# API configuration
API_HOST = "0.0.0.0"
API_PORT = 8000

# LangSmith configuration
LANGSMITH_PROJECT_NAME = "rbi-nbfc-chatbot"
