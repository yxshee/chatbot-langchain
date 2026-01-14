# 🚀 RBI NBFC Chatbot - Quick Reference Guide

## ⚡ Quick Start Commands

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env and add: GOOGLE_API_KEY=your_key_here

# Verify setup
python scripts/check.py
```

### Run the Chatbot

```bash
# 🌐 Web Interface (Best for most users)
streamlit run app.py

# 💬 Interactive CLI
python examples/demo_interactive.py

# 🔌 REST API Server
python examples/demo_api.py

# 📚 FAQ Demo
python examples/demo_faq.py

# ⚡ Quick Test
python scripts/quick_start.py
```

### Testing
```bash
# Health check
python scripts/check.py

# Complete test
python tests/test_complete_system.py

# RAG pipeline test
python tests/test_rag_pipeline.py

# All tests with pytest
pytest
```

---

## 🏗️ Architecture in 30 Seconds

```
USER → STREAMLIT/CLI/API → RAG CHAIN → [RETRIEVER + LLM] → RESPONSE
                                            ↓         ↓
                                         FAISS    GEMINI
                                        (716     (2.5 Flash)
                                        chunks)
```

**Data Flow:**
1. User asks question
2. Question → 768-dim vector (embedding)
3. FAISS finds top 4 similar chunks
4. Chunks + Question → Gemini
5. Gemini generates answer
6. Answer + citations → User

---

## 🛠️ Tech Stack Summary

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **LLM** | Google Gemini 2.5 Flash | Generate answers |
| **Embeddings** | text-embedding-004 (768-dim) | Convert text to vectors |
| **Vector DB** | FAISS | Fast similarity search |
| **Framework** | LangChain 0.2.16 | Orchestrate RAG pipeline |
| **Web UI** | Streamlit 1.37+ | Interactive interface |
| **API** | FastAPI 0.112 | REST endpoints |
| **PDF Processing** | PyPDF, PyMuPDF | Extract text |
| **Monitoring** | LangSmith | Track & evaluate |

---

## 📁 Project Structure (Simplified)

```
chatbot-langchain/
├── app.py                              # Streamlit web interface
├── requirements.txt                    # Dependencies
├── .env                               # API keys (create from .env.example)
│
├── src/rbi_nbfc_chatbot/              # Main package
│   ├── chains/                        # RAG pipeline
│   │   ├── rag_chain.py              # Main logic
│   │   └── retriever.py              # FAISS search
│   ├── utils/                         # Utilities
│   │   └── ingest.py                 # Process PDFs
│   ├── api/                          # FastAPI server
│   └── config.py                     # Settings
│
├── examples/                          # Demo scripts
├── tests/                            # Test suite
├── scripts/                          # Utility scripts
│
└── data/
    ├── documents/                    # Source PDFs
    │   └── rbi_nbfc_master_direction.pdf
    └── vector_store/                 # FAISS index
        └── index.faiss
```

---

## 🔑 Key Concepts

### What is RAG (Retrieval-Augmented Generation)?
RAG combines:
1. **Retrieval**: Find relevant information (FAISS searches 716 chunks)
2. **Augmentation**: Add context to the prompt
3. **Generation**: LLM creates answer based on retrieved context

**Why RAG?**
- ✅ Reduces hallucinations (answers grounded in real docs)
- ✅ Provides citations (shows sources)
- ✅ Works with custom documents (your PDFs)
- ✅ More accurate than pure LLM

### How Embeddings Work
```
Text: "What is an NBFC?"
  ↓ (embedding model)
Vector: [0.023, -0.145, 0.089, ..., 0.234]  (768 numbers)
  ↓ (similarity search)
Find similar document vectors in FAISS
```

### FAISS Index
- **What**: Facebook AI Similarity Search
- **Contains**: 716 document chunks as vectors
- **Purpose**: Lightning-fast similarity search (<100ms)
- **How**: Compares query vector with all chunk vectors

### The RAG Chain
```python
# Simplified version of what happens:
1. retriever = create_retriever()           # Load FAISS
2. docs = retriever.get_relevant_docs(q)    # Search
3. context = format_docs(docs)               # Prepare
4. prompt = f"Context: {context}\nQ: {q}"   # Build prompt
5. answer = llm.generate(prompt)             # Generate
6. return {"answer": answer, "sources": docs}
```

---

## ⚙️ Configuration Quick Reference

### Environment Variables (.env)
```env
GOOGLE_API_KEY=your_key              # Required
GEMINI_MODEL=gemini-2.5-flash        # LLM model
TEMPERATURE=0.1                       # 0-1 (lower = factual)
RETRIEVAL_K=4                         # Number of chunks
```

### Key Parameters

| Parameter | Default | What it does |
|-----------|---------|--------------|
| `TEMPERATURE` | 0.1 | Creativity (0=factual, 1=creative) |
| `RETRIEVAL_K` | 4 | Number of chunks to retrieve |
| `CHUNK_SIZE` | 1000 | Characters per chunk |
| `CHUNK_OVERLAP` | 200 | Overlap between chunks |

---

## 🐛 Troubleshooting

### Common Issues

**"API Key Error"**
```bash
# Solution: Add key to .env
echo 'GOOGLE_API_KEY=your_key_here' >> .env
```

**"FAISS index not found"**
```bash
# Solution: Rebuild vector store
python -m src.rbi_nbfc_chatbot.utils.ingest
```

**"Import errors"**
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt
```

**"Slow responses"**
```bash
# Solution: Reduce retrieval number
# In .env: RETRIEVAL_K=2
```

---

## 📊 Performance Stats

- **Query Time**: 2-5 seconds
- **Vector Search**: <100ms
- **LLM Generation**: 1-4 seconds
- **Memory Usage**: ~4GB
- **Document Chunks**: 716
- **Embedding Dimensions**: 768

---

## 🎯 Example Queries

Try these questions:

1. **Definitions**
   - "What is a Non-Banking Financial Company?"
   - "Define Net Owned Fund"

2. **Requirements**
   - "What is the minimum capital requirement for NBFCs?"
   - "Can NBFCs accept demand deposits?"

3. **Regulations**
   - "What is the Scale Based Regulatory Framework?"
   - "What are the prudential norms for NBFCs?"

4. **Comparisons**
   - "What are the differences between banks and NBFCs?"
   - "How do NBFC classifications differ?"

---

## 🌐 API Usage

### Query Endpoint
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is an NBFC?",
    "return_sources": true
  }'
```

### Response Format
```json
{
  "answer": "A Non-Banking Financial Company...",
  "sources": [
    {
      "content": "Full text...",
      "page": 12,
      "source": "rbi_nbfc_master_direction.pdf"
    }
  ]
}
```

---

## 🧪 Testing Workflow

```bash
# 1. Quick health check
python scripts/check.py

# 2. Test a single question
python scripts/quick_start.py

# 3. Run FAQ demo
python examples/demo_faq.py

# 4. Complete system test
python tests/test_complete_system.py

# 5. Interactive testing
python examples/demo_interactive.py
```

---

## 📚 Documentation Files

- **PROJECT_DOCUMENTATION.md**: Complete, detailed documentation
- **QUICK_REFERENCE.md**: This file - quick commands & concepts
- **README.md**: Project overview and quick start
- **.env.example**: Environment variables template

---

## 🚀 Deployment Checklist

- [ ] API keys configured in `.env`
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Vector store exists (`data/vector_store/index.faiss`)
- [ ] Health check passes (`python scripts/check.py`)
- [ ] Test query works (`python scripts/quick_start.py`)
- [ ] Web UI accessible (`streamlit run app.py`)

---

## 🔗 Useful Links

- **Google AI Studio**: https://makersuite.google.com/app/apikey
- **LangSmith Dashboard**: https://smith.langchain.com
- **LangChain Docs**: https://python.langchain.com
- **FAISS Documentation**: https://github.com/facebookresearch/faiss
- **Streamlit Gallery**: https://streamlit.io/gallery

---

## 💡 Pro Tips

1. **Better Answers**: Be specific in questions
   - ❌ "Tell me about NBFCs"
   - ✅ "What is the minimum Net Owned Fund requirement for NBFCs?"

2. **Verify Sources**: Always check the retrieved excerpts
   - Click "Show sources" to see exact text
   - Check page numbers for verification

3. **Adjust Parameters**:
   - Low temperature (0.1) → Factual, consistent
   - High temperature (0.7) → Creative, varied
   - More chunks (k=6) → More context, slower
   - Fewer chunks (k=2) → Faster, less context

4. **Export Chats**: Use "Export chat" button to save conversations

5. **Monitor Performance**: Enable LangSmith to track all queries

---

## 🎓 Learning Path

1. **Start**: Run `python scripts/quick_start.py`
2. **Explore**: Try the web UI with sample questions
3. **Understand**: Read the architecture section
4. **Code**: Look at `src/rbi_nbfc_chatbot/chains/rag_chain.py`
5. **Customize**: Modify parameters in `.env`
6. **Advanced**: Add new features or documents

---

**Questions? Check PROJECT_DOCUMENTATION.md for comprehensive details!**

*Last Updated: January 2026*
