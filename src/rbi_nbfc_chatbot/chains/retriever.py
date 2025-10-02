"""Document retriever for RBI NBFC Chatbot.

This module creates and manages the FAISS retriever for document search.
"""

import os
from typing import Optional
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema.retriever import BaseRetriever

from ..config import (
    GOOGLE_API_KEY,
    EMBEDDING_MODEL,
    VECTOR_STORE_PATH,
    RETRIEVAL_K
)


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
    
    # Initialize embeddings
    embeddings = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=api_key
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


def get_relevant_documents(query: str, retriever: Optional[BaseRetriever] = None):
    """
    Retrieve relevant documents for a query.
    
    Args:
        query: Search query
        retriever: Retriever instance (if None, creates new one)
    
    Returns:
        List of relevant documents
    """
    if retriever is None:
        retriever = create_retriever()
    
    return retriever.get_relevant_documents(query)
