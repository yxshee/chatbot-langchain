# 🏦 RBI NBFC Chatbot - Intelligent Regulatory Assistant

> **A sophisticated RAG-powered chatbot** using Google Gemini AI, FAISS vector search, and 716 document chunks from official RBI guidelines.

---

## 🚀 Quick Start (3 Commands)

```bash
# 1. Setup
pip install -r requirements.txt
cp .env.example .env  # Add your GOOGLE_API_KEY

# 2. Quick test
python scripts/quick_start.py

# 3. Choose your interface:
streamlit run streamlit_app.py          # Web UI (recommended)
python examples/demo_interactive.py     # CLI chat
python examples/demo_api.py             # API server
python examples/demo_faq.py             # FAQ demo
```

---

## 📋 What This Does

✨ **330-page RBI Master Direction** → **716 smart chunks** → **Accurate answers with citations**

### Interfaces Available:

| Interface | Command | Use Case |
|-----------|---------|----------|
| **🌐 Web UI** | `streamlit run streamlit_app.py` | Best for demos, presentations |
| **💬 Interactive CLI** | `python examples/demo_interactive.py` | Quick Q&A sessions |
| **🔌 REST API** | `python examples/demo_api.py` | Integration, automation |
| **📚 FAQ Demo** | `python examples/demo_faq.py` | Pre-loaded questions |

---

## 🔧 Complete Testing

```bash
# Quick system check
python scripts/check.py

# Complete test suite
python tests/test_complete_system.py

# Individual tests
python tests/test_rag_pipeline.py
```

---

## 📊 Technical Stack

- **LLM**: Google Gemini 2.5 Flash
- **Embeddings**: Google text-embedding-004 (768-dim)
- **Vector DB**: FAISS (716 chunks)
- **Framework**: LangChain 0.2.16
- **API**: FastAPI + Streamlit

---

## 🎯 Key Features

✅ **716 optimized chunks** from RBI Master Direction  
✅ **4-document retrieval** for accurate context  
✅ **Source attribution** for all answers  
✅ **Multiple interfaces** (Web, CLI, API)  
✅ **Production-ready** error handling  
✅ **LangSmith integration** for evaluation  

---

## 🔑 Configuration

Create `.env` file:

```env
GOOGLE_API_KEY=your_google_api_key_here
LANGSMITH_API_KEY=your_langsmith_key_here  # Optional
GEMINI_MODEL=gemini-2.5-flash
RETRIEVAL_K=4
```

Get API keys:
- Google AI: https://makersuite.google.com/app/apikey
- LangSmith: https://smith.langchain.com/settings

---

## 📁 Project Structure

```
chatbot-langchain/
├── streamlit_app.py              # Web UI
├── src/rbi_nbfc_chatbot/        # Core package
│   ├── chains/                  # RAG pipeline
│   ├── utils/                   # Document processing
│   ├── api/                     # FastAPI server
│   └── evals/                   # Evaluation tools
├── examples/                     # Demo scripts
├── tests/                        # Test suite
├── data/                         # Vector store & documents
└── scripts/                      # Utility scripts
```

---

## 🎥 Video Demonstration Flow

1. **Quick Start**: `python scripts/quick_start.py`
2. **FAQ Demo**: `python examples/demo_faq.py`
3. **Interactive Chat**: `python examples/demo_interactive.py`
4. **Web UI**: `streamlit run streamlit_app.py`
5. **API Testing**: `python examples/demo_api.py`
6. **Full Tests**: `python tests/test_complete_system.py`

---

## 🔍 Troubleshooting

| Issue | Solution |
|-------|----------|
| API Key Error | Add `GOOGLE_API_KEY` to `.env` |
| FAISS Not Found | Run `python -m src.rbi_nbfc_chatbot.utils.ingest` |
| Import Errors | `pip install -r requirements.txt` |
| Wrong Model | Use `gemini-1.5-flash` in `.env` |

**Quick Fix**: `python scripts/check.py` for diagnosis

---

## 📈 Performance

- ⚡ **2-5 seconds** per query
- 🎯 **716 chunks** searchable
- 🔍 **Top-4** document retrieval
- 💾 **~4GB** memory usage

---

## 📚 Evaluation

```bash
# Run comprehensive evaluation
python -m src.rbi_nbfc_chatbot.evals.langsmith_eval

# Or import and use
from src.rbi_nbfc_chatbot.evals import run_evaluation
run_evaluation()
```

View results on [LangSmith Dashboard](https://smith.langchain.com)

---

**Built with ❤️ using Google Gemini, LangChain, and FAISS**
