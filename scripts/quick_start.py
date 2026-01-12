"""Quick start script to test everything works."""

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

def main():
    print("="*70)
    print("RBI NBFC CHATBOT - QUICK START")
    print("="*70)
    print()
    
    # Check environment
    print("1. Checking environment...")
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY not set in .env file")
        print("   Please add your API key to .env")
        return False
    print("✅ API key configured")
    print()
    
    # Check data files
    print("2. Checking data files...")
    from src.rbi_nbfc_chatbot.config import PDF_PATH, FAISS_INDEX_PATH
    
    if not PDF_PATH.exists():
        print(f"❌ PDF not found at {PDF_PATH}")
        return False
    print(f"✅ PDF found")
    
    if not FAISS_INDEX_PATH.exists():
        print(f"⚠️  FAISS index not found")
        print("   Building vector store...")
        try:
            from src.rbi_nbfc_chatbot.utils import ingest_documents
            ingest_documents(force=True)
            print("✅ Vector store built")
        except Exception as e:
            print(f"❌ Failed to build vector store: {e}")
            return False
    else:
        print("✅ Vector store exists")
    print()
    
    # Test RAG chain
    print("3. Testing RAG chain...")
    try:
        from src.rbi_nbfc_chatbot.chains import build_rag_chain
        
        rag_chain = build_rag_chain()
        
        question = "What is an NBFC?"
        print(f"   Question: {question}")
        
        response = rag_chain.ask_question(question)
        
        print(f"   Answer: {response['answer'][:150]}...")
        print("✅ RAG chain working")
    except Exception as e:
        print(f"❌ RAG chain failed: {e}")
        return False
    print()
    
    # Success
    print("="*70)
    print("✅ QUICK START COMPLETE - System is working!")
    print("="*70)
    print()
    print("Next steps:")
    print("  1. Interactive chat: python examples/demo_interactive.py")
    print("  2. FAQ demo: python examples/demo_faq.py")
    print("  3. Web UI: streamlit run streamlit_app.py")
    print("  4. API server: python examples/demo_api.py")
    print("  5. Full tests: python tests/test_complete_system.py")
    print()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
