"""
Comprehensive project status checker
Run this before creating your submission
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def check_status():
    """Check all project components"""
    print("\n" + "="*80)
    print("RBI NBFC CHATBOT - PROJECT STATUS CHECK")
    print("="*80 + "\n")
    
    all_good = True
    
    # 1. Environment
    print("1️⃣  ENVIRONMENT CONFIGURATION")
    print("─"*80)
    
    gemini_key = os.getenv("GOOGLE_API_KEY")
    langsmith_key = os.getenv("LANGSMITH_API_KEY")
    
    if gemini_key and len(gemini_key) > 20:
        print("   ✅ Gemini API Key configured")
    else:
        print("   ❌ Gemini API Key missing or invalid")
        all_good = False
    
    if langsmith_key and len(langsmith_key) > 20:
        print("   ✅ LangSmith API Key configured")
    else:
        print("   ❌ LangSmith API Key missing or invalid")
        all_good = False
    
    # 2. Data Files
    print("\n2️⃣  DATA FILES")
    print("─"*80)
    
    pdf_path = Path("data/documents/rbi_nbfc_master_direction.pdf")
    if pdf_path.exists():
        print(f"   ✅ PDF file present ({pdf_path.stat().st_size / 1024 / 1024:.1f} MB)")
    else:
        print("   ❌ PDF file missing")
        all_good = False
    
    faiss_path = Path("data/vector_store/index.faiss")
    if faiss_path.exists():
        print(f"   ✅ FAISS index built")
    else:
        print("   ❌ FAISS index not built - run: python -m src.rbi_nbfc_chatbot.utils.ingest")
        all_good = False
    
    # 3. Core Components
    print("\n3️⃣  CORE COMPONENTS")
    print("─"*80)
    
    components = {
        "PDF Ingestion": "src/rbi_nbfc_chatbot/utils/ingest.py",
        "RAG Chain": "src/rbi_nbfc_chatbot/chains/rag_chain.py",
        "Retriever": "src/rbi_nbfc_chatbot/chains/retriever.py",
        "API Server": "src/rbi_nbfc_chatbot/api/server.py",
        "CLI Demo": "examples/demo_cli.py",
        "Interactive Demo": "examples/demo_interactive.py",
        "API Demo": "examples/demo_api.py",
        "FAQ Demo": "examples/demo_faq.py",
        "Test Suite": "tests/test_rag_pipeline.py",
    }
    
    for name, path in components.items():
        if Path(path).exists():
            print(f"   ✅ {name}")
        else:
            print(f"   ❌ {name} missing")
            all_good = False
    
    # 4. Evaluation Components
    print("\n4️⃣  EVALUATION COMPONENTS")
    print("─"*80)
    
    eval_components = {
        "LangSmith Evaluator": "src/rbi_nbfc_chatbot/evals/langsmith_eval.py",
    }
    
    for name, path in eval_components.items():
        if Path(path).exists():
            print(f"   ✅ {name}")
        else:
            print(f"   ❌ {name} missing")
            all_good = False
    
    # 5. Dependencies
    print("\n5️⃣  CRITICAL DEPENDENCIES")
    print("─"*80)
    
    deps = [
        ("langchain", "langchain"),
        ("langchain-google-genai", "langchain_google_genai"),
        ("faiss-cpu", "faiss"),
        ("fastapi", "fastapi"),
        ("pypdf", "pypdf"),
        ("python-dotenv", "dotenv"),
        ("langsmith", "langsmith"),
    ]
    
    for pkg_name, import_name in deps:
        try:
            __import__(import_name)
            print(f"   ✅ {pkg_name}")
        except ImportError:
            print(f"   ❌ {pkg_name} - run: pip install {pkg_name}")
            all_good = False
    
    # 6. Functionality Tests
    print("\n6️⃣  FUNCTIONALITY TESTS")
    print("─"*80)
    
    print("   ℹ️  Run these commands to test:")
    print("      python tests/test_rag_pipeline.py          # Test core chatbot")
    print("      python examples/demo_faq.py                # Demo FAQ answers")
    print("      python examples/demo_interactive.py        # Interactive chat")
    print("      python examples/demo_api.py                # Web API")
    print("      python examples/demo_cli.py                # CLI demo")
    
    # 7. Evaluation Status
    print("\n7️⃣  EVALUATION STATUS")
    print("─"*80)
    
    print("   ℹ️  Run these commands for evaluation:")
    print("      python -m src.rbi_nbfc_chatbot.evals.langsmith_eval")
    print("      # Or import and use: from src.rbi_nbfc_chatbot.evals import run_evaluation")
    
    # Summary
    print("\n" + "="*80)
    if all_good:
        print("✅ PROJECT STATUS: READY FOR SUBMISSION")
        print("="*80)
        print("\n📹 READY TO RECORD VIDEO!")
        print("\nSuggested demo flow:")
        print("  1. Run: python examples/demo_faq.py           # FAQ demonstration")
        print("  2. Run: python tests/test_rag_pipeline.py     # Test pipeline")
        print("  3. Run: python examples/demo_interactive.py   # Interactive chat")
        print("  4. Run: python examples/demo_api.py           # Web API server")
        print("  5. Show: http://localhost:8000/docs           # API documentation")
        print("  6. Run: python examples/demo_cli.py           # CLI demo")
        print("\n📦 PROJECT READY FOR DEPLOYMENT")
    else:
        print("⚠️  PROJECT STATUS: NEEDS ATTENTION")
        print("="*80)
        print("\nPlease fix the issues marked with ❌ above")
    
    print()

if __name__ == "__main__":
    check_status()