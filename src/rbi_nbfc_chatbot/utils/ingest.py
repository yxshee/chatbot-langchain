"""Document ingestion and vector store creation."""

import os
from typing import Optional, List
from pathlib import Path
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document

from .document_loader import load_pdf, split_documents
from ..config import (
    GOOGLE_API_KEY,
    EMBEDDING_MODEL,
    VECTOR_STORE_PATH,
    PDF_PATH
)


def build_vector_store(
    documents: List[Document],
    api_key: Optional[str] = None,
    output_path: Optional[str] = None
) -> FAISS:
    """
    Build a FAISS vector store from documents.
    
    Args:
        documents: List of document chunks
        api_key: Google API key (default: from config)
        output_path: Path to save the vector store (default: from config)
    
    Returns:
        FAISS vector store instance
    """
    api_key = api_key or GOOGLE_API_KEY
    output_path = output_path or VECTOR_STORE_PATH
    
    if not api_key:
        raise ValueError("Google API key is required. Set GOOGLE_API_KEY in .env file")
    
    # Initialize embeddings
    embeddings = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=api_key
    )
    
    # Create vector store
    print(f"Creating vector store from {len(documents)} document chunks...")
    vectorstore = FAISS.from_documents(documents, embeddings)
    
    # Save vector store
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    vectorstore.save_local(output_path)
    print(f"✅ Vector store saved to {output_path}")
    
    return vectorstore


def ingest_documents(
    pdf_path: Optional[str] = None,
    output_path: Optional[str] = None,
    api_key: Optional[str] = None,
    force: bool = False
) -> FAISS:
    """
    Complete document ingestion pipeline.
    
    Loads PDF, splits into chunks, creates embeddings, and saves vector store.
    
    Args:
        pdf_path: Path to PDF file (default: from config)
        output_path: Path to save vector store (default: from config)
        api_key: Google API key (default: from config)
        force: Force re-ingestion even if vector store exists
    
    Returns:
        FAISS vector store instance
    
    Raises:
        FileNotFoundError: If PDF file doesn't exist
    """
    pdf_path = pdf_path or str(PDF_PATH)
    output_path = output_path or VECTOR_STORE_PATH
    
    # Check if vector store already exists
    if not force and os.path.exists(output_path):
        print(f"Vector store already exists at {output_path}")
        print("Use force=True to re-ingest")
        
        # Load existing vector store
        api_key = api_key or GOOGLE_API_KEY
        embeddings = GoogleGenerativeAIEmbeddings(
            model=EMBEDDING_MODEL,
            google_api_key=api_key
        )
        vectorstore = FAISS.load_local(
            output_path,
            embeddings,
            allow_dangerous_deserialization=True
        )
        return vectorstore
    
    print("=" * 70)
    print("📚 DOCUMENT INGESTION PIPELINE")
    print("=" * 70)
    
    # Step 1: Load PDF
    print(f"\n1️⃣ Loading PDF: {pdf_path}")
    documents = load_pdf(pdf_path)
    print(f"   ✅ Loaded {len(documents)} pages")
    
    # Step 2: Split into chunks
    print(f"\n2️⃣ Splitting documents into chunks...")
    chunks = split_documents(documents)
    print(f"   ✅ Created {len(chunks)} chunks")
    
    # Step 3: Build vector store
    print(f"\n3️⃣ Building vector store...")
    vectorstore = build_vector_store(chunks, api_key=api_key, output_path=output_path)
    
    print("\n" + "=" * 70)
    print("✅ INGESTION COMPLETE!")
    print("=" * 70)
    print(f"📄 Pages: {len(documents)}")
    print(f"📦 Chunks: {len(chunks)}")
    print(f"💾 Vector store: {output_path}")
    print("=" * 70)
    
    return vectorstore


if __name__ == "__main__":
    """Run ingestion as standalone script."""
    import sys
    
    try:
        ingest_documents(force=True)
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
