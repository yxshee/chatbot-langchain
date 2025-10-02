#!/usr/bin/env python
"""Test script for RAG pipeline using modular structure."""

import os
import sys

# Add src to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

# Load environment
load_dotenv()

# Test 1: Import and test model directly
print("=" * 60)
print("TEST 1: Testing Gemini Model Connection")
print("=" * 60)

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    
    # Get API key from environment
    api_key = os.getenv("GOOGLE_API_KEY")
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    
    print(f"Using model: {model_name}")
    print(f"API Key: {api_key[:10]}..." if api_key else "No API key")
    
    # Initialize model
    llm = ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=api_key,
        temperature=0.1
    )
    
    # Test model
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
    
    # Test embedding
    test_text = "This is a test"
    embedding = embeddings.embed_query(test_text)
    print(f"✅ Generated embedding of length: {len(embedding)}")
    
except Exception as e:
    print(f"❌ Embeddings test failed: {e}")

# Test 3: Test FAISS Vector Store
print("\n" + "=" * 60)
print("TEST 3: Testing FAISS Vector Store Retrieval")
print("=" * 60)

try:
    from langchain_community.vectorstores import FAISS
    
    index_path = os.getenv("FAISS_INDEX_PATH", "data/index.faiss")
    
    print(f"Loading FAISS index from: {index_path}")
    
    # Load vector store
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004",
        google_api_key=api_key
    )
    
    vectorstore = FAISS.load_local(
        index_path,
        embeddings,
        allow_dangerous_deserialization=True
    )
    
    # Test retrieval
    test_question = "What are the capital requirements for NBFCs?"
    docs = vectorstore.similarity_search(test_question, k=2)
    
    print(f"✅ Retrieved {len(docs)} documents")
    print(f"Sample content: {docs[0].page_content[:150]}...")
    
except Exception as e:
    print(f"❌ FAISS test failed: {e}")

# Test 4: End-to-end RAG Query
print("\n" + "=" * 60)
print("TEST 4: Testing Complete RAG Pipeline")
print("=" * 60)

try:
    from langchain.chains import RetrievalQA
    from langchain.prompts import PromptTemplate
    
    # Create prompt
    prompt_template = """You are an expert on RBI NBFC regulations. 
    
Context:
{context}

Question: {question}

Answer based only on the context above:"""
    
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )
    
    # Create retriever
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    # Create QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )
    
    # Test query
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
