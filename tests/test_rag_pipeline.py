#!/usr/bin/env python
"""RAG pipeline smoke test.

This file is primarily intended to be run as a script:
    python tests/test_rag_pipeline.py

It used to execute API-calling code at import time, which is problematic for
pytest collection. The logic is now contained in `main()`.
"""

import os
import sys

# Add src to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

# Load environment
load_dotenv()

def main() -> int:
    # Test 1: Import and test model directly
    print("=" * 60)
    print("TEST 1: Testing Gemini Model Connection")
    print("=" * 60)

    api_key = os.getenv("GOOGLE_API_KEY")
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    print(f"Using model: {model_name}")
    print("API Key: configured" if api_key else "API Key: not configured")

    try:
        from langchain_google_genai import ChatGoogleGenerativeAI

        llm = ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=api_key,
            temperature=0.1
        )
        response = llm.invoke("Say 'Model is working!' if you can read this.")
        print(f"✅ Model Response: {response.content}")
    except Exception as e:
        print(f"❌ Model test failed: {e}")

    # Test 2: Test Embeddings
    print("\n" + "=" * 60)
    print("TEST 2: Testing Gemini Embeddings")
    print("=" * 60)

    try:
        from langchain_google_genai import GoogleGenerativeAIEmbeddings

        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004",
            google_api_key=api_key
        )
        embedding = embeddings.embed_query("This is a test")
        print(f"✅ Generated embedding of length: {len(embedding)}")
    except Exception as e:
        print(f"❌ Embeddings test failed: {e}")

    # Test 3: Test FAISS Vector Store
    print("\n" + "=" * 60)
    print("TEST 3: Testing FAISS Vector Store Retrieval")
    print("=" * 60)

    vectorstore = None
    try:
        from langchain_community.vectorstores import FAISS
        from langchain_google_genai import GoogleGenerativeAIEmbeddings

        index_path = os.getenv("FAISS_INDEX_PATH", "data/vector_store/index.faiss")
        print(f"Loading FAISS index from: {index_path}")

        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004",
            google_api_key=api_key
        )

        vectorstore = FAISS.load_local(
            index_path,
            embeddings,
            allow_dangerous_deserialization=True
        )

        docs = vectorstore.similarity_search("What are the capital requirements for NBFCs?", k=2)
        print(f"✅ Retrieved {len(docs)} documents")
        print(f"Sample content: {docs[0].page_content[:150]}...")
    except Exception as e:
        print(f"❌ FAISS test failed: {e}")

    # Test 4: End-to-end RAG Query
    print("\n" + "=" * 60)
    print("TEST 4: Testing Complete RAG Pipeline")
    print("=" * 60)

    try:
        if vectorstore is None:
            raise RuntimeError("Vector store not loaded; skipping end-to-end test")

        from langchain.chains import RetrievalQA
        from langchain.prompts import PromptTemplate
        from langchain_google_genai import ChatGoogleGenerativeAI

        llm = ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=api_key,
            temperature=0.1
        )

        prompt = PromptTemplate(
            template=(
                "You are an expert on RBI NBFC regulations.\n\n"
                "Context:\n{context}\n\n"
                "Question: {question}\n\n"
                "Answer based only on the context above:"
            ),
            input_variables=["context", "question"],
        )

        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            chain_type_kwargs={"prompt": prompt},
            return_source_documents=True
        )

        question = "What is the minimum Net Owned Fund requirement for NBFCs?"
        result = qa_chain({"query": question})

        print(f"Question: {question}")
        print(f"✅ Answer: {result['result']}")
        print(f"✅ Sources: {len(result['source_documents'])} documents")
    except Exception as e:
        print(f"❌ RAG pipeline test failed: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 60)
    print("TESTING COMPLETE")
    print("=" * 60)

    return 0


def test_imports_only():
    """Pytest-safe smoke test: verify module imports without executing API calls."""
    from src.rbi_nbfc_chatbot.chains import build_rag_chain  # noqa: F401


if __name__ == "__main__":
    raise SystemExit(main())
