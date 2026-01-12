"""Document retriever for RBI NBFC Chatbot.

This module creates and manages the FAISS retriever for document search.
"""

import os
from typing import Optional
import faiss

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema.retriever import BaseRetriever

from ..config import (
    GOOGLE_API_KEY,
    GOOGLE_EMBEDDING_MODEL,
    VECTOR_STORE_PATH,
    RETRIEVAL_K
)


def _read_faiss_dimension(index_path: str) -> Optional[int]:
    """Read the dimension (d) from a FAISS index on disk, if present."""
    try:
        candidate = os.path.join(index_path, "index.faiss")
        if os.path.exists(candidate):
            idx = faiss.read_index(candidate)
            return int(getattr(idx, "d", 0)) or None
    except Exception:
        return None
    return None


def create_retriever(
    index_path: Optional[str] = None,
    k: Optional[int] = None,
    api_key: Optional[str] = None
) -> BaseRetriever:
    """
    Create a FAISS retriever for document search.
    
    Args:
        index_path: Path to FAISS index directory (default: from config)
        k: Number of documents to retrieve (default: from config)
        api_key: Google API key (default: from config)
    
    Returns:
        BaseRetriever: Configured FAISS retriever
    
    Raises:
        FileNotFoundError: If FAISS index doesn't exist
        ValueError: If API key is missing
    """
    # Use defaults from config
    index_path = index_path or VECTOR_STORE_PATH
    k = k or RETRIEVAL_K

    api_key = api_key or GOOGLE_API_KEY
    if not api_key:
        raise ValueError("Google API key is required. Set GOOGLE_API_KEY in .env file")
    
    if not os.path.exists(index_path):
        raise FileNotFoundError(
            f"FAISS index not found at {index_path}. "
            "Please run document ingestion first."
        )

    # Sanity check: bundled index is created with Gemini embeddings (768-d).
    index_dim = _read_faiss_dimension(index_path)
    if index_dim is not None and index_dim != 768:
        raise ValueError(
            f"The FAISS index on disk is {index_dim}-dimensional, but this project is configured "
            "for Gemini embeddings (768-d). Rebuild the vector store with the provided ingestion pipeline."
        )

    # Initialize embeddings
    embeddings = GoogleGenerativeAIEmbeddings(
        model=GOOGLE_EMBEDDING_MODEL,
        google_api_key=api_key,
    )
    
    # Load vector store
    vectorstore = FAISS.load_local(
        index_path,
        embeddings,
        allow_dangerous_deserialization=True
    )
    
    # Create and return retriever
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": k}
    )
    
    return retriever
