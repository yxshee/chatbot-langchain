#!/usr/bin/env python
"""Interactive RBI NBFC Chatbot - Chat directly with the bot!"""

import os
import sys

# Add src to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

from src.rbi_nbfc_chatbot.chains import build_rag_chain

# Load environment
load_dotenv()

print("=" * 70)
print("🤖 RBI NBFC CHATBOT - INTERACTIVE MODE")
print("=" * 70)
print()

# Initialize components
print("🔄 Loading chatbot components...")

try:
    # Build RAG chain using modular structure
    rag_chain = build_rag_chain()

    print("✅ Chatbot loaded successfully!")
    print()
    print("=" * 70)
    print("💬 You can now ask questions about RBI NBFC regulations")
    print("📝 Type 'quit', 'exit', or 'q' to stop")
    print("=" * 70)
    print()

    # Sample questions to show user
    print("💡 Example questions you can ask:")
    print("   - What are the capital requirements for NBFCs?")
    print("   - Can an NBFC accept demand deposits?")
    print("   - What is the Net Owned Fund requirement?")
    print("   - What are the prudential norms for NBFCs?")
    print()
    print("=" * 70)
    print()

    # Interactive loop
    conversation_count = 0

    while True:
        try:
            # Get user input
            question = input("🙋 Your Question: ").strip()

            # Check for exit commands
            if question.lower() in ['quit', 'exit', 'q', 'bye']:
                print()
                print("👋 Thank you for using RBI NBFC Chatbot!")
                print(f"📊 You asked {conversation_count} question(s)")
                print()
                break

            # Skip empty input
            if not question:
                continue

            # Process question
            print()
            print("🔍 Searching RBI documents...")

            response = rag_chain.ask_question(question, return_sources=True)

            conversation_count += 1

            # Display answer
            print()
            print("🤖 Answer:")
            print("-" * 70)
            print(response['answer'])
            print("-" * 70)

            # Display sources
            sources = response.get('sources', [])
            print(f"📚 Based on {len(sources)} source document(s)")
            print()

            # Show brief source preview
            if sources:
                print("📄 Source Preview:")
                preview = sources[0]['content'][:200]
                print(f"   {preview}...")
                print()

            print("=" * 70)
            print()

        except KeyboardInterrupt:
            print()
            print()
            print("👋 Interrupted. Thank you for using RBI NBFC Chatbot!")
            print(f"📊 You asked {conversation_count} question(s)")
            print()
            break

        except Exception as e:
            print()
            print(f"❌ Error: {e}")
            print("Please try asking your question differently.")
            print()
            print("=" * 70)
            print()

except Exception as e:
    print()
    print(f"❌ Failed to initialize chatbot: {e}")
    print()
    print("Please ensure:")
    print("1. Virtual environment is activated: source .venv/bin/activate")
    print("2. API key is configured in .env file")
    print("3. Vector database exists at data/vector_store/index.faiss/")
    print()
    sys.exit(1)
