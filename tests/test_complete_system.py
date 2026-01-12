"""Complete system test for RBI NBFC Chatbot."""

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

def check_1_environment() -> bool:
    """Check 1: Environment Configuration.

    Returns:
        bool: True if environment looks configured for an online run, else False.
    """
    print("\n" + "="*70)
    print("TEST 1: Environment Configuration")
    print("="*70)
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        # When executed under pytest (e.g., CI), skip instead of hard-failing.
        # When executed as a standalone script, this test will still show up as failed
        # in the summary.
        try:
            import pytest  # type: ignore
            pytest.skip("GOOGLE_API_KEY not configured")
        except Exception:
            print("❌ GOOGLE_API_KEY not set")
            return False
    if len(api_key) <= 20:
        try:
            import pytest  # type: ignore
            pytest.skip("GOOGLE_API_KEY seems invalid (too short)")
        except Exception:
            print("❌ GOOGLE_API_KEY seems invalid")
            return False
    print("✅ Environment variables configured")
    return True


def test_1_environment():
    """Test 1: Environment Configuration"""
    assert check_1_environment() is True

def check_2_imports() -> bool:
    """Check 2: Import All Modules."""
    print("\n" + "="*70)
    print("TEST 2: Module Imports")
    print("="*70)
    
    try:
        from src.rbi_nbfc_chatbot import config
        print("✅ Config module")
        
        from src.rbi_nbfc_chatbot.chains import build_rag_chain, RAGChain
        print("✅ Chain modules")
        
        from src.rbi_nbfc_chatbot.utils import ingest_documents
        print("✅ Utility modules")
        
        from src.rbi_nbfc_chatbot.api import app
        print("✅ API module")
        
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False


def test_2_imports():
    """Test 2: Import All Modules"""
    assert check_2_imports() is True

def check_3_data_files() -> bool:
    """Check 3: Data Files."""
    print("\n" + "="*70)
    print("TEST 3: Data Files")
    print("="*70)
    
    from src.rbi_nbfc_chatbot.config import PDF_PATH, FAISS_INDEX_PATH
    
    if PDF_PATH.exists():
        size_mb = PDF_PATH.stat().st_size / 1024 / 1024
        print(f"✅ PDF file exists ({size_mb:.1f} MB)")
    else:
        print(f"❌ PDF file missing at {PDF_PATH}")
        return False
    
    if FAISS_INDEX_PATH.exists():
        print("✅ FAISS index exists")
    else:
        print(f"⚠️  FAISS index not found at {FAISS_INDEX_PATH}")
        print("   Run: python -m src.rbi_nbfc_chatbot.utils.ingest")
        return False
    
    return True


def test_3_data_files():
    """Test 3: Data Files"""
    assert check_3_data_files() is True

def check_4_embeddings() -> bool:
    """Check 4: Embeddings Generation."""
    print("\n" + "="*70)
    print("TEST 4: Embeddings Generation")
    print("="*70)
    
    try:
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        from src.rbi_nbfc_chatbot.config import GOOGLE_API_KEY, EMBEDDING_MODEL
        
        embeddings = GoogleGenerativeAIEmbeddings(
            model=EMBEDDING_MODEL,
            google_api_key=GOOGLE_API_KEY
        )
        
        test_text = "What is an NBFC?"
        embedding = embeddings.embed_query(test_text)
        
        print(f"✅ Generated embedding (dimension: {len(embedding)})")
        return True
    except Exception as e:
        print(f"❌ Embeddings test failed: {e}")
        return False


def test_4_embeddings():
    """Test 4: Embeddings Generation"""
    assert check_4_embeddings() is True

def check_5_retriever() -> bool:
    """Check 5: Document Retrieval."""
    print("\n" + "="*70)
    print("TEST 5: Document Retrieval")
    print("="*70)
    
    try:
        from src.rbi_nbfc_chatbot.chains import create_retriever
        
        retriever = create_retriever()
        
        question = "What is an NBFC?"
        # get_relevant_documents is deprecated; prefer invoke.
        docs = retriever.invoke(question)
        
        print(f"✅ Retrieved {len(docs)} documents")
        print(f"   Sample: {docs[0].page_content[:100]}...")
        return True
    except Exception as e:
        print(f"❌ Retriever test failed: {e}")
        return False


def test_5_retriever():
    """Test 5: Document Retrieval"""
    assert check_5_retriever() is True

def check_6_llm() -> bool:
    """Check 6: LLM Connection."""
    print("\n" + "="*70)
    print("TEST 6: LLM Connection")
    print("="*70)
    
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        from src.rbi_nbfc_chatbot.config import GEMINI_MODEL, GOOGLE_API_KEY
        
        llm = ChatGoogleGenerativeAI(
            model=GEMINI_MODEL,
            google_api_key=GOOGLE_API_KEY,
            temperature=0.1
        )
        
        response = llm.invoke("Say 'LLM working' if you can read this.")
        print(f"✅ LLM Response: {response.content}")
        return True
    except Exception as e:
        print(f"❌ LLM test failed: {e}")
        return False


def test_6_llm():
    """Test 6: LLM Connection"""
    assert check_6_llm() is True

def check_7_rag_chain() -> bool:
    """Check 7: Complete RAG Chain."""
    print("\n" + "="*70)
    print("TEST 7: Complete RAG Chain")
    print("="*70)
    
    try:
        from src.rbi_nbfc_chatbot.chains import build_rag_chain
        
        rag_chain = build_rag_chain()
        
        question = "What is the minimum capital requirement for NBFCs?"
        response = rag_chain.ask_question(question)
        
        print(f"✅ Question: {question}")
        print(f"✅ Answer: {response['answer'][:200]}...")
        print(f"✅ Sources: {len(response.get('sources', []))} documents")
        return True
    except Exception as e:
        print(f"❌ RAG chain test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_7_rag_chain():
    """Test 7: Complete RAG Chain"""
    assert check_7_rag_chain() is True

def check_8_api() -> bool:
    """Check 8: API Server."""
    print("\n" + "="*70)
    print("TEST 8: API Server")
    print("="*70)
    
    try:
        from src.rbi_nbfc_chatbot.api import app
        print("✅ API app imported successfully")
        print("   Start with: uvicorn src.rbi_nbfc_chatbot.api.server:app --port 8000")
        return True
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False


def test_8_api():
    """Test 8: API Server"""
    assert check_8_api() is True

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*70)
    print("RBI NBFC CHATBOT - COMPLETE SYSTEM TEST")
    print("="*70)
    
    checks = [
        check_1_environment,
        check_2_imports,
        check_3_data_files,
        check_4_embeddings,
        check_5_retriever,
        check_6_llm,
        check_7_rag_chain,
        check_8_api,
    ]
    
    results = []
    for check in checks:
        try:
            result = check()
            results.append(result)
        except Exception as e:
            print(f"❌ Test crashed: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(results)
    total = len(results)
    
    print(f"\n✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    if all(results):
        print("\n🎉 ALL TESTS PASSED! System is fully functional.")
        print("\n📹 Ready for video demonstration!")
    else:
        print("\n⚠️  Some tests failed. Please fix issues above.")
    
    print("="*70 + "\n")
    
    return all(results)

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
