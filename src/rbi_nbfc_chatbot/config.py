"""Configuration module for RBI NBFC Chatbot."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
DOCUMENTS_DIR = DATA_DIR / "documents"
VECTOR_STORE_DIR = DATA_DIR / "vector_store"

# PDF file path
PDF_PATH = DOCUMENTS_DIR / "rbi_nbfc_master_direction.pdf"

# FAISS index path
FAISS_INDEX_PATH = VECTOR_STORE_DIR / "index.faiss"

# API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")

# Model configuration
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "models/text-embedding-004")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.1"))

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
