#!/usr/bin/env python3
"""
Simple demo script for RBI NBFC Chatbot
Shows key functionality for video demonstration
"""

import os
import sys
import time

# Add src to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from src.rbi_nbfc_chatbot.chains import create_retriever

# Load environment variables
load_dotenv()

def demo_retrieval():
    """Demo the retrieval functionality"""
    print("🔍 DEMO: Document Retrieval")
    print("=" * 50)
    
    try:
        # Initialize retriever
        print("📚 Loading FAISS vector database...")
        retriever = create_retriever()
        print("✅ Vector database loaded successfully!")
        
        # Test questions
        questions = [
            "Can an NBFC accept demand deposits?",
            "What are the capital requirements for NBFCs?",
            "What is the definition of NBFC?"
        ]
        
        for i, question in enumerate(questions, 1):
            print(f"\n🔍 Question {i}: {question}")
            print("-" * 40)
            
            # Retrieve relevant documents
            docs = retriever.invoke(question)
            print(f"📄 Found {len(docs)} relevant documents")
            
            # Show first document snippet
            if docs:
                content = docs[0].page_content[:200] + "..."
                print(f"📖 Sample context: {content}")
            
        print("\n" + "=" * 50)
        print("✅ Retrieval demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Error in retrieval demo: {e}")

def demo_summary():
    """Show project summary"""
    print("\n🎯 PROJECT SUMMARY")
    print("=" * 50)
    print("✅ PDF Ingestion: 330 pages → 716 chunks")
    print("✅ Vector Database: FAISS with Gemini embeddings")
    print("✅ RAG Pipeline: LangChain + Gemini API")
    print("✅ API Server: FastAPI with /ask endpoint")
    print("✅ Evaluation: LangSmith integration ready")
    print("\n📊 TECHNICAL STACK")
    print("- LLM: Google Gemini 1.5 Flash")
    print("- Embeddings: text-embedding-004")
    print("- Vector Store: FAISS")
    print("- Framework: LangChain")
    print("- API: FastAPI")
    print("- Evaluation: LangSmith")
    print("\n🎥 Ready for video demonstration!")

if __name__ == "__main__":
    print("🤖 RBI NBFC CHATBOT DEMO")
    print("=" * 50)
    print("This demo shows the core functionality for video presentation")
    print("=" * 50)
    
    # Run demos
    demo_retrieval()
    demo_summary()
    
    print("\n📋 NEXT STEPS FOR VIDEO:")
    print("1. Show this retrieval demo")
    print("2. Start FastAPI server: uvicorn src.app:app --port 8000")
    print("3. Test API with curl or browser")
    print("4. Show LangSmith evaluation setup")
    print("5. Demonstrate end-to-end pipeline")
    print("\n🎬 Ready to record!")