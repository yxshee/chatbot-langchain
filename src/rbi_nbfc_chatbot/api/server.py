"""FastAPI server for RBI NBFC Chatbot."""

import time
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ..chains import RAGChain, build_rag_chain
from ..config import API_HOST, API_PORT, GEMINI_MODEL


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan handler.

    Replaces deprecated @app.on_event("startup") while keeping the same behavior:
    attempt to initialize the RAG chain at startup, but fall back to lazy init.
    """
    print("=" * 70)
    print("🚀 RBI NBFC Chatbot API Starting...")
    print("=" * 70)

    try:
        get_rag_chain()
        print("✅ API ready to accept requests!")
    except Exception as e:
        print(f"⚠️  Warning: Could not initialize chatbot on startup: {e}")
        print("   Chatbot will be initialized on first request.")

    print("=" * 70)
    print("📡 API Endpoints:")
    print("   GET  /          - API information")
    print("   GET  /health    - Health check")
    print("   POST /ask       - Ask a question")
    print("   GET  /docs      - Interactive API documentation")
    print("=" * 70)

    yield


# Initialize FastAPI app
app = FastAPI(
    title="RBI NBFC Chatbot API",
    description="Ask questions about RBI NBFC regulations using RAG pipeline",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class QuestionRequest(BaseModel):
    """Request model for asking questions."""
    question: str
    max_sources: Optional[int] = 4

class QuestionResponse(BaseModel):
    """Response model for answers."""
    question: str
    answer: str
    sources: List[Dict[str, Any]]
    timestamp: str
    model: str
    processing_time_ms: float

# Global RAG chain (lazy loaded)
_rag_chain: Optional[RAGChain] = None


def get_rag_chain() -> RAGChain:
    """Get or initialize the RAG chain."""
    global _rag_chain

    if _rag_chain is None:
        print("🔄 Initializing RAG chain...")
        _rag_chain = build_rag_chain()
        print("✅ RAG chain initialized!")

    return _rag_chain


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "RBI NBFC Chatbot API",
        "version": "2.0.0",
        "status": "running",
        "description": "Ask questions about RBI NBFC regulations",
        "endpoints": {
            "/": "API information (this page)",
            "/health": "Health check",
            "/ask": "Ask a question (POST)",
            "/docs": "Interactive API documentation",
            "/redoc": "Alternative API documentation"
        },
        "example": {
            "method": "POST",
            "url": "/ask",
            "body": {
                "question": "What are the capital requirements for NBFCs?",
                "max_sources": 4
            }
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "chatbot_initialized": _rag_chain is not None,
        "model": GEMINI_MODEL,
        "provider": "google",
    }


@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """
    Ask a question about RBI NBFC regulations.
    
    This endpoint uses a Retrieval-Augmented Generation (RAG) pipeline to:
    1. Retrieve relevant context from RBI Master Direction document
    2. Generate accurate answers using Google Gemini
    3. Provide source attribution
    
    Example request:
    ```json
    {
        "question": "What are the capital requirements for NBFCs?",
        "max_sources": 4
    }
    ```
    
    Example response:
    ```json
    {
        "question": "What are the capital requirements for NBFCs?",
        "answer": "NBFCs must maintain a minimum Capital Adequacy Ratio...",
        "sources": [...],
        "timestamp": "2025-04-23T10:30:00",
        "model": "gemini-2.5-flash",
        "processing_time_ms": 1250.5
    }
    ```
    """
    start_time = time.time()

    try:
        # Get RAG chain
        rag_chain = get_rag_chain()

        # Process question
        response = rag_chain.ask_question(request.question, return_sources=True)

        # Limit sources to requested amount
        sources = response.get("sources", [])[:request.max_sources]

        # Format sources for API response
        formatted_sources = [
            {
                "chunk_id": i + 1,
                "content": src["content"][:300] + "..." if len(src["content"]) > 300 else src["content"],
                "page": src["page"],
                "source": src.get("source", "RBI Master Direction")
            }
            for i, src in enumerate(sources)
        ]

        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000

        return QuestionResponse(
            question=request.question,
            answer=response["answer"],
            sources=formatted_sources,
            timestamp=datetime.now().isoformat(),
            model=response["model"],
            processing_time_ms=round(processing_time, 2)
        )

    except FileNotFoundError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Vector store not found. Please run document ingestion first. Error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing question: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn

    print(f"🌐 Starting server at http://{API_HOST}:{API_PORT}")
    print(f"📝 API Documentation: http://{API_HOST}:{API_PORT}/docs")
    print()

    uvicorn.run(app, host=API_HOST, port=API_PORT)
