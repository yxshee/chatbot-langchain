#!/usr/bin/env python3
"""
Rebuild the Gemini FAISS vector store.

This is equivalent to running the ingestion pipeline with force=True.
"""

import sys
from pathlib import Path

# Add project root
sys.path.insert(0, str(Path(__file__).parent.parent))

print("Starting vector store rebuild (Gemini embeddings)...")
print("=" * 80)

try:
    from dotenv import load_dotenv
    load_dotenv()

    print("✅ Environment loaded")

    from src.rbi_nbfc_chatbot.utils.ingest import ingest_documents

    print("✅ Modules imported")
    print("\nRebuilding vector store with Gemini embeddings...")
    print("This will take 5-10 minutes...\n")

    vectorstore = ingest_documents(force=True)

    print("\n" + "=" * 80)
    print("✅ SUCCESS! Vector store rebuilt with Gemini embeddings")
    print("=" * 80)
    print("\nYou can now run the chatbot:")
    print("  streamlit run streamlit_app.py")
    print("  python examples/demo_interactive.py")
    print("  python examples/demo_faq.py")
    print()

except KeyboardInterrupt:
    print("\n\n⚠️  Rebuild interrupted by user")
    sys.exit(1)
except Exception as e:
    print(f"\n\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
