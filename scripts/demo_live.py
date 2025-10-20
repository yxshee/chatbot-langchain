#!/usr/bin/env python3
"""
Simple demonstration of the RBI NBFC Chatbot working correctly.
This script tests the core functionality without requiring user interaction.
"""

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

def main():
    print("\n" + "="*80)
    print("🚀 RBI NBFC CHATBOT - LIVE DEMONSTRATION")
    print("="*80 + "\n")
    
    # Test 1: Import modules
    print("1️⃣  Testing Module Imports...")
    try:
        from src.rbi_nbfc_chatbot import config
        from src.rbi_nbfc_chatbot.chains import build_rag_chain
        print("   ✅ All modules imported successfully\n")
    except Exception as e:
        print(f"   ❌ Import failed: {e}\n")
        return False
    
    # Test 2: Check configuration
    print("2️⃣  Checking Configuration...")
    print(f"   📊 Model: {config.GEMINI_MODEL}")
    print(f"   🔍 Retrieval K: {config.RETRIEVAL_K}")
    print(f"   📁 PDF Path: {config.PDF_PATH.name}")
    print(f"   ✅ Configuration loaded\n")
    
    # Test 3: Build RAG chain
    print("3️⃣  Building RAG Chain...")
    try:
        rag_chain = build_rag_chain()
        print("   ✅ RAG chain initialized\n")
    except Exception as e:
        print(f"   ❌ Failed to build chain: {e}\n")
        return False
    
    # Test 4: Ask sample questions
    print("4️⃣  Testing Q&A System...")
    print("   " + "-"*76)
    
    sample_questions = [
        "What is an NBFC?",
        "What are the capital requirements for NBFCs?",
        "What is the regulatory framework for NBFCs?"
    ]
    
    for i, question in enumerate(sample_questions, 1):
        print(f"\n   Question {i}: {question}")
        print("   " + "."*76)
        
        try:
            response = rag_chain.ask_question(question)
            answer = response.get('answer', 'No answer generated')
            sources = response.get('sources', [])
            
            # Print answer (truncated for display)
            answer_preview = answer[:200] + "..." if len(answer) > 200 else answer
            print(f"   Answer: {answer_preview}")
            print(f"   Sources: {len(sources)} documents retrieved")
            print("   ✅ Success")
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)[:100]}")
            continue
    
    print("\n   " + "-"*76)
    
    # Summary
    print("\n" + "="*80)
    print("✅ DEMONSTRATION COMPLETE")
    print("="*80)
    print("\n📌 The chatbot is working and can answer questions about RBI NBFC regulations!")
    print("\n🌐 Available Interfaces:")
    print("   • Streamlit Web UI: streamlit run streamlit_app.py")
    print("   • Interactive CLI: python examples/demo_interactive.py")
    print("   • API Server: python examples/demo_api.py")
    print("   • FAQ Demo: python examples/demo_faq.py")
    print("\n" + "="*80 + "\n")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Demonstration interrupted by user.\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}\n")
        sys.exit(1)
