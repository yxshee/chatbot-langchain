# 🏦 RBI NBFC Chatbot - Intelligent Regulatory Assistant

> **25-word description**: A sophisticated RAG-powered chatbot that answers RBI NBFC regulatory questions using Google Gemini AI, FAISS vector search, and 716 document chunks from official RBI guidelines.

---

## 🎯 What This Does

✨ **Processes 330-page RBI Master Direction** → **716 smart chunks** → **Accurate answers with citations**

🎨 **Multiple Interfaces**: CLI 💻 | Web API 🌐 | Streamlit UI 🎭 | Demo Modes 🎬

📊 **Evaluation Framework**: LangSmith integration with 23 FAQ questions

🏆 **Production-Ready**: Error handling, logging, comprehensive testing

---

## 🚀 Quick Start (3 Steps)

### 1. Setup Environment
```bash
pip install -r requirements.txt
cp .env.example .env  # Add your API keys
```

### 2. Verify Everything Works
```bash
python scripts/check.py  # ✅ All systems go?
```

### 3. Launch Your Interface
```bash
# 🌐 Web App (Recommended)
streamlit run streamlit_app.py

# 💻 CLI Chat
python examples/demo_interactive.py

# 🔌 API Server
python examples/demo_api.py
```

---

## 🎮 Usage Options

| Interface | Command | Perfect For |
|-----------|---------|-------------|
| **🌐 Streamlit Web** | `streamlit run streamlit_app.py` | Interactive browsing, demos |
| **💻 CLI Chat** | `python examples/demo_interactive.py` | Quick testing, development |
| **� REST API** | `python examples/demo_api.py` | Integration, automation |
| **🎬 FAQ Demo** | `python examples/demo_faq.py` | Presentations, videos |

---

## 🛠️ Technical Stack

### 🤖 AI Models
- **LLM**: Google Gemini 2.5 Flash (`gemini-2.5-flash`)
- **Embeddings**: Google `text-embedding-004` (768-dim)
- **Vector DB**: FAISS (716 chunks, k=4 retrieval)

### 🏗️ Architecture
```
📄 RBI PDF (330 pages)
    ↓
🔍 Smart Text Splitting (1000 chars + 200 overlap)
    ↓
🧮 Google Embeddings → FAISS Vector Store
    ↓
❓ User Question → Vector Search → Context Retrieval
    ↓
🤖 Gemini AI → Answer Generation + Source Citations
    ↓
💬 Response with References
```

---

## 📋 Prerequisites

- ✅ Python 3.10+
- ✅ Google API Key ([Get here](https://makersuite.google.com/app/apikey))
- ✅ LangSmith API Key ([Optional](https://smith.langchain.com/settings))
- ✅ 8GB RAM recommended

---

## 🔧 Configuration

### Environment Variables (`.env`)
```bash
GOOGLE_API_KEY=your_google_api_key_here
LANGSMITH_API_KEY=your_langsmith_api_key_here  # Optional
```

### Key Settings
- **Model**: `gemini-2.5-flash` (deterministic, temp=0.1)
- **Retrieval**: Top-4 most relevant chunks
- **Chunk Size**: 1000 characters with 200 overlap

---

## � Evaluation & Testing

### Run Evaluations
```bash
# Create dataset (23 RBI FAQ questions)
python -m src.evals.build_dataset_from_rbi_faq

# Run comprehensive evaluation
python -m src.evals.run_eval --dataset "RBI-NBFC-FAQ-v1"
```

### Metrics Tracked
- 🎯 **Correctness**: Answer accuracy vs reference
- 🔗 **Faithfulness**: Grounded in source documents
- 🎪 **Relevancy**: Addresses the question
- 📏 **Conciseness**: Appropriate answer length

**View Results**: [LangSmith Dashboard](https://smith.langchain.com)

---

## 📁 Project Structure

```
🏗️ chatbot-langchain/
├── 🎨 streamlit_app.py          # Web interface
├── 🔌 src/rbi_nbfc_chatbot/     # Core modules
│   ├── 🤖 chains/               # RAG pipeline
│   ├── 🔍 utils/                # PDF processing
│   └── 📊 evals/                # Evaluation system
├── 📚 data/                     # Vector store & documents
├── 🎬 examples/                 # Demo scripts
├── 🧪 tests/                    # Test suite
└── 📖 docs/                     # Documentation
```

---

## 🎥 Demo Scripts

### Interactive FAQ Demo
```bash
python examples/demo_faq.py
```
Shows 10 carefully selected questions with full pipeline demonstration.

### CLI System Test
```bash
python examples/demo_cli.py
```
Comprehensive testing: model connection → embeddings → retrieval → answers.

### API Testing
```bash
# Start server
python examples/demo_api.py

# Test endpoint
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"What is NBFC capital requirement?"}'
```

---

## 🔍 Troubleshooting

### Common Issues & Fixes

| Problem | Solution |
|---------|----------|
| 🔑 **API Key Error** | Add `GOOGLE_API_KEY=your_key` to `.env` |
| 📁 **FAISS Not Found** | Run `python -m src.rbi_nbfc_chatbot.utils.ingest` |
| 📦 **Import Errors** | `pip install -r requirements.txt` |
| 🔌 **Port 8000 Busy** | Change port: `--port 8001` |
| 🤖 **Wrong Model** | Use `gemini-2.5-flash` in config |

### Verification Commands
```bash
python scripts/check.py           # Full system check
python tests/test_rag_pipeline.py # Pipeline test
python examples/demo_cli.py       # Quick functionality test
```

---

## � Performance

- ⚡ **Response Time**: 2-5 seconds per question
- 🎯 **Accuracy**: Evaluated with LangSmith metrics
- 📊 **Vector Store**: 716 optimized chunks
- 🔍 **Retrieval**: Top-4 relevant documents
- 💾 **Memory**: ~4GB for vector store

---

## 🎬 Video Recording Guide

### Recording Flow (15 minutes)
1. **Intro** (2min): Project overview, tech stack
2. **Components** (4min): Explain RAG pipeline, models, vector search
3. **Demos** (6min): FAQ demo, interactive chat, API testing
4. **Evaluation** (2min): LangSmith metrics, dataset creation
5. **Wrap-up** (1min): Final status, key achievements

### Pro Tips
- 🎥 Use Loom or screen recorder at 1080p
- 🗣️ Speak clearly, explain each step
- 💻 Maximize terminal for clarity
- 🎯 Show actual outputs, not just commands

---

## 📚 Key Concepts

- **🔍 RAG**: Retrieval-Augmented Generation combines search + AI
- **🧮 Embeddings**: Text converted to numerical vectors for similarity
- **⚡ FAISS**: Facebook's fast vector similarity search
- **🔗 LangChain**: Framework for LLM applications
- **📊 LangSmith**: Evaluation and monitoring platform

---

## � Important Notes

- 📄 **Source**: RBI Master Direction – NBFC (Scale Based Regulation) Directions
- ❓ **FAQ Data**: Official RBI NBFC FAQ (April 23, 2025)
- 🧪 **Testing**: 23 questions covering key regulatory topics
- 🤖 **Model**: Google Gemini 2.5 Flash for production use
- 🛠️ **Framework**: LangChain 0.2.16 with compatible dependencies

---

## 🤝 Support

**Need Help?**
1. Run `python scripts/check.py` for diagnostics
2. Check terminal logs for error details
3. Verify `.env` has correct API keys
4. Ensure FAISS index exists in `data/vector_store/`

---

**Built with ❤️ using Google Gemini, LangChain, and FAISS**
