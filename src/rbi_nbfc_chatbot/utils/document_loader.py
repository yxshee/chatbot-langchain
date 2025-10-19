"""Document loading utilities for PDF processing."""

from typing import List
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

from ..config import CHUNK_SIZE, CHUNK_OVERLAP, PDF_PATH


def load_pdf(pdf_path: str = None) -> List[Document]:
    """
    Load a PDF file and extract its content.
    
    Args:
        pdf_path: Path to PDF file (default: from config)
    
    Returns:
        List of Document objects
    
    Raises:
        FileNotFoundError: If PDF file doesn't exist
    """
    pdf_path = pdf_path or str(PDF_PATH)
    
    if not Path(pdf_path).exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    
    return documents


def split_documents(
    documents: List[Document],
    chunk_size: int = None,
    chunk_overlap: int = None
) -> List[Document]:
    """
    Split documents into chunks for embedding.
    
    Args:
        documents: List of documents to split
        chunk_size: Size of each chunk (default: from config)
        chunk_overlap: Overlap between chunks (default: from config)
    
    Returns:
        List of chunked documents
    """
    chunk_size = chunk_size or CHUNK_SIZE
    chunk_overlap = chunk_overlap or CHUNK_OVERLAP
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = text_splitter.split_documents(documents)
    
    return chunks
