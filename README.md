# 🏦 RBI NBFC Chatbot - Intelligent Regulatory Assistant

A production-ready RAG (Retrieval-Augmented Generation) chatbot that answers questions about RBI NBFC regulations using Google Gemini 2.5 Flash and LangChain. Built for precision, reliability, and compliance in financial regulatory queries.

## 🎯 What This Project Does

This chatbot processes the **330-page RBI Master Direction on NBFC regulations** and provides:
- ✅ **Accurate answers** to regulatory questions with source citations
- ✅ **Vector search** across 716 document chunks using FAISS
- ✅ **Multiple interfaces**: CLI, Web API, and demonstration modes
- ✅ **Evaluation framework** using LangSmith with 23 FAQ questions
- ✅ **Production-ready code** with error handling and logging

**Perfect for**: Compliance teams, NBFC operators, financial analysts, and regulatory researchers.

---

## 🚀 Complete Setup Guide (From Zero to Running)

### Prerequisites
- Python 3.10 or higher
- Google API Key (for Gemini)
- LangSmith API Key (optional, for evaluations)
- 8GB RAM recommended
- macOS, Linux, or Windows

### Step 1: Clone/Download Project

```bash
cd /path/to/your/workspace
# Project should be in: /Users/venom/Downloads/proj2
```

### Step 2: Create Virtual Environment

```bash
python -m venv .venv

# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Expected packages**:
- langchain==0.2.16
- langchain-google-genai
- langchain-community
- faiss-cpu
- pypdf
- fastapi
- uvicorn
- python-dotenv
- langsmith

### Step 4: Configure Environment Variables

```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your API keys
nano .env  # or use any text editor
```

**Required variables in `.env`**:
```bash
GOOGLE_API_KEY=your_google_api_key_here
LANGSMITH_API_KEY=your_langsmith_api_key_here  # Optional
```

**Get API Keys**:
- Google Gemini: https://makersuite.google.com/app/apikey
- LangSmith: https://smith.langchain.com/settings

### Step 5: Process RBI PDF (If Not Already Done)

**Skip this step if `data/vector_store/index.faiss/` already exists**

```bash
python -m src.rbi_nbfc_chatbot.utils.ingest
```

This will:
- Load the 330-page RBI NBFC Master Direction PDF
- Split into 716 chunks with smart text splitting
- Generate embeddings using Google text-embedding-004
- Create FAISS vector store in `data/vector_store/index.faiss/`

**Expected output**: `✅ Successfully created FAISS index with 716 documents`

### Step 6: Verify Everything Works

```bash
python scripts/check.py
```

This comprehensive checker will verify:
- ✅ API keys configured
- ✅ PDF file present
- ✅ FAISS index built
- ✅ All core components exist
- ✅ Dependencies installed

### Step 7: Run Quick Tests

```bash
# Test retrieval
python examples/demo_cli.py

# Test full pipeline
python tests/test_rag_pipeline.py
```

**Expected**: Both should run without errors ✅

---

## 🎮 Usage Guide

### Option 1: Interactive Chatbot (Recommended for First Use)

```bash
python examples/demo_interactive.py
```

**What it does**:
- Provides a welcoming chat interface
- Shows example questions
- Allows you to ask questions interactively
- Displays answers with source citations
- Type `exit`, `quit`, or press Ctrl+C to stop

**Example session**:
```
💬 RBI NBFC Chatbot
Ask me anything about RBI NBFC regulations!

You: What is the minimum capital requirement for NBFCs?

🤖 Answer:
NBFCs are required to maintain a minimum Net Owned Fund (NOF) of Rs.2 crore...
[Shows source citations]
```

### Option 2: FAQ Demonstration (Best for Video)

```bash
python examples/demo_faq.py
```

**What it does**:
- Runs through 10 carefully selected FAQ questions
- Shows the complete RAG pipeline in action
- Displays retrieval, answer generation, and sources
- Perfect for demonstration videos
- Press Enter to move between questions

**Questions demonstrated**:
1. What is a Non-Banking Financial Company (NBFC)?
2. What are the key differences between banks and NBFCs?
3. Does an NBFC require RBI approval to commence business?
4. What is the minimum Net Owned Fund (NOF) requirement?
5. What is the Capital Adequacy Ratio requirement?
6. Can NBFCs accept deposits from public?
7. What is meant by a Systemically Important NBFC?
8. What are the prudential norms for asset classification?
9. What are the KYC/AML requirements?
10. What are the penalties for non-compliance?

### Option 3: Web API Server

```bash
python examples/demo_api.py
```

**What it does**:
- Starts FastAPI server on port 8000
- Provides REST API endpoint: `POST /ask`
- Includes Swagger UI at: http://localhost:8000/docs
- Supports JSON request/response
- Production-ready with error handling

**Test the API**:
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"What are the regulatory reporting requirements for NBFCs?"}'
```

**Or visit**: http://localhost:8000/docs for interactive API testing

### Option 4: CLI Demo

```bash
python examples/demo_cli.py
```

**What it does**:
- Runs a comprehensive system test
- Tests model connection (Gemini)
- Tests embeddings generation
- Tests FAISS retrieval
- Tests complete RAG pipeline
- Shows example question with answer

---

## 🔬 Evaluation System

### Step 1: Create Evaluation Dataset

```bash
# Create dataset with all 23 questions
python -m src.evals.build_dataset_from_rbi_faq

# Or create with limited questions for testing
python -m src.evals.build_dataset_from_rbi_faq --limit 5 --dataset-name "RBI-Test"
```

**What it does**:
- Creates LangSmith dataset with 23 FAQ questions
- Includes expected answers for evaluation
- Questions sourced from official RBI FAQ (April 23, 2025)
- Dataset visible at: https://smith.langchain.com

### Step 2: Run Evaluations

```bash
python -m src.evals.run_eval --dataset "RBI-NBFC-FAQ-v1"
```

**What it does**:
- Runs chatbot on all questions in dataset
- Evaluates with 4 metrics:
  - ✅ **Correctness**: Answer matches reference
  - ✅ **Faithfulness**: Answer grounded in sources
  - ✅ **Relevancy**: Answer addresses question
  - ✅ **Conciseness**: Appropriate answer length
- Results visible in LangSmith dashboard
- Generates experiment with timestamp

**View results**: https://smith.langchain.com

---

## 📁 Project Structure

```
proj2/
├── 106MDNBFCS1910202343073E3EF57A4916AA5042911CD8D562.pdf  # RBI Master Direction (330 pages)
├── .env                                # Environment variables (API keys)
├── .env.example                        # Template for .env
├── requirements.txt                    # Python dependencies
├── check.py                            # Project status checker
├── demo.py                             # Basic demo
├── demo_faq.py                         # FAQ demonstration (10 questions)
├── api_server.py                       # FastAPI web server
├── chatbot_interactive.py              # Interactive CLI chatbot
├── test_working.py                     # Comprehensive system test
├── QUICKSTART.md                       # Quick reference guide
├── FINAL_STATUS.md                     # Implementation status
│
├── data/
│   └── index.faiss/                    # FAISS vector store (716 chunks)
│       ├── index.faiss                 # Vector index
│       └── index.pkl                   # Metadata
│
├── configs/
│   └── prompt_rubric.md                # Evaluation prompts
│
└── src/
    ├── __init__.py
    ├── app.py                          # FastAPI application
    │
    ├── chains/
    │   ├── __init__.py
    │   ├── rag_chain.py                # RAG pipeline with Gemini
    │   └── retriever.py                # FAISS retriever setup
    │
    ├── utils/
    │   ├── __init__.py
    │   ├── ingest.py                   # PDF → FAISS ingestion
    │   └── io_helpers.py               # Utility functions
    │
    └── evals/
        ├── __init__.py
        ├── build_dataset_from_rbi_faq.py  # Create evaluation dataset (23 FAQs)
        └── run_eval.py                    # Run LangSmith evaluations
```

---

## 🎥 Video Recording Guide (Loom Demonstration)

### Recording Setup

**Tools needed**:
- Loom (https://www.loom.com) or any screen recorder
- Terminal window (maximized for clarity)
- Web browser (for API docs and LangSmith)

**Recording tips**:
- Use 1080p resolution
- Speak clearly and explain as you go
- Keep video between 10-15 minutes
- Show output clearly (use `clear` command between demos)

### Suggested Video Flow (15 minutes)

#### Part 1: Introduction (2 minutes)
```bash
# Show project structure
ls -la

# Show status check
python check.py
```

**What to say**:
- "This is an RAG chatbot for RBI NBFC regulations"
- "Built with Google Gemini, LangChain, and FAISS"
- "Processes 330-page RBI Master Direction into 716 chunks"
- "Let me show you all the components..."

#### Part 2: Component Explanation (4 minutes)

**Explain each component**:

1. **PDF Ingestion** (`src/utils/ingest.py`):
   - "Loads 330-page RBI PDF"
   - "Splits into 716 chunks using RecursiveCharacterTextSplitter"
   - "Generates embeddings with Google text-embedding-004"
   - "Creates FAISS vector store for fast retrieval"

2. **FAISS Retriever** (`src/chains/retriever.py`):
   - "Loads vector store from disk"
   - "Configured with k=4 (retrieves 4 most relevant chunks)"
   - "Returns documents with metadata (page numbers, source)"

3. **RAG Chain** (`src/chains/rag_chain.py`):
   - "Integrates retriever with Gemini 2.5 Flash"
   - "Custom prompt template for regulatory queries"
   - "Temperature 0.1 for deterministic answers"
   - "Returns answer with source citations"

4. **Evaluation System** (`src/evals/`):
   - "23 FAQ questions from official RBI FAQ"
   - "LangSmith integration for evaluation"
   - "4 metrics: correctness, faithfulness, relevancy, conciseness"

#### Part 3: Live Demonstrations (6 minutes)

**Demo 1: FAQ Demonstration**
```bash
python demo_faq.py
```

**What to show**:
- Run through 2-3 questions (not all 10)
- Highlight: question → retrieval → answer → sources
- Point out source citations and page numbers
- Show model being used (Gemini 2.5 Flash)

**Demo 2: Interactive Chatbot**
```bash
python chatbot_interactive.py
```

**What to show**:
- Ask 2-3 custom questions, e.g.:
  - "What are the licensing requirements for NBFCs?"
  - "Explain the Asset Liability Management framework"
- Show how it handles questions
- Demonstrate graceful exit

**Demo 3: Web API**
```bash
# In one terminal:
python api_server.py

# In browser:
# Visit http://localhost:8000/docs
```

**What to show**:
- Swagger UI interface
- POST /ask endpoint
- Test with a question in the UI
- Show JSON response with answer and sources

#### Part 4: Evaluation System (2 minutes)

```bash
# Create test dataset
python -m src.evals.build_dataset_from_rbi_faq --limit 3 --dataset-name "Demo-Dataset"

# Run evaluation
python -m src.evals.run_eval --dataset "Demo-Dataset" --experiment-name "video-demo"
```

**What to say**:
- "Creates dataset with FAQ questions and expected answers"
- "Runs chatbot on all questions"
- "Evaluates with 4 metrics automatically"
- "Results visible in LangSmith dashboard"
- (Show LangSmith dashboard if possible)

#### Part 5: Wrap-up (1 minute)

```bash
# Show final status
python check.py
```

**What to say**:
- "All components working seamlessly"
- "Production-ready implementation"
- "Google Gemini for LLM and embeddings"
- "LangChain for RAG pipeline"
- "FAISS for vector storage"
- "LangSmith for evaluation"
- "Thank you for watching!"

---

## 🔧 Technical Details

### Models Used

- **LLM**: Google Gemini 2.5 Flash (`gemini-2.5-flash`)
  - Temperature: 0.1 (low for deterministic regulatory answers)
  - Used for answer generation
  
- **Embeddings**: Google `text-embedding-004`
  - Dimension: 768
  - Used for vector search in FAISS

### RAG Pipeline

1. **User asks question** → Question is sent to RAG chain
2. **Vector search** → FAISS retrieves k=4 most similar chunks
3. **Context + Prompt** → Retrieved chunks + custom prompt template
4. **LLM generation** → Gemini generates answer based on context
5. **Response** → Answer + source citations returned

### Performance Metrics

- **Vector Store**: 716 chunks from 330-page PDF
- **Retrieval**: Top-4 most relevant documents (k=4)
- **Chunk size**: 1000 characters with 200 overlap
- **Response time**: ~2-5 seconds per question
- **Accuracy**: Evaluated using LangSmith metrics

---

## �� Troubleshooting

### Common Issues

**1. "GOOGLE_API_KEY not found"**
```bash
# Solution: Add API key to .env
echo 'GOOGLE_API_KEY=your_key_here' >> .env
```

**2. "FAISS index not found"**
```bash
# Solution: Run ingestion
python -m src.utils.ingest
```

**3. "ImportError: No module named 'xyz'"**
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt
```

**4. "Model 'gemini-1.5-flash' not found"**
- The correct model is: `gemini-2.5-flash`
- Check `src/chains/rag_chain.py` line ~67

**5. "Port 8000 already in use"**
```bash
# Solution: Kill process or use different port
python api_server.py --port 8001
```

### Verification Commands

```bash
# Check all components
python check.py

# Test RAG pipeline
python test_working.py

# Test single question
python demo.py
```

---

## 📊 Evaluation Metrics Explained

### 1. Correctness
**What it measures**: How well the generated answer matches the expected reference answer.

**How it works**:
- Extracts key phrases from reference answer
- Checks how many appear in generated answer
- Bonus for high string similarity
- Score: 0.0 to 1.0

### 2. Faithfulness
**What it measures**: Whether the answer is grounded in retrieved source documents.

**How it works**:
- Splits answer into sentences
- Checks if each sentence is supported by sources
- Penalizes hallucinations (unsupported claims)
- Score: 0.0 to 1.0

### 3. Relevancy
**What it measures**: Whether the answer addresses the question asked.

**How it works**:
- Extracts key terms from question
- Checks how many are addressed in answer
- Ensures answer is on-topic
- Score: 0.0 to 1.0

### 4. Conciseness
**What it measures**: Whether the answer is appropriately detailed (not too short/long).

**How it works**:
- Compares answer length to reference
- Optimal: 80-120% of reference length
- Penalizes very short or very long answers
- Score: 0.0 to 1.0

---

## 🎓 Learning Resources

### Understanding the Code

- **RAG Pipeline**: `src/chains/rag_chain.py` - Start here to understand the flow
- **Vector Search**: `src/chains/retriever.py` - See how FAISS retrieval works
- **PDF Processing**: `src/utils/ingest.py` - Learn document chunking
- **Evaluation**: `src/evals/run_eval.py` - Understand metric computation

### Key Concepts

- **RAG (Retrieval-Augmented Generation)**: Combines retrieval (FAISS) with generation (Gemini)
- **Vector Embeddings**: Numerical representations of text for similarity search
- **FAISS**: Facebook AI Similarity Search for fast vector lookups
- **LangChain**: Framework for building LLM applications
- **LangSmith**: Platform for LLM evaluation and monitoring

---

## 📝 Notes

- **PDF Source**: RBI Master Direction – NBFC (Scale Based Regulation) Directions
- **FAQ Source**: Official RBI NBFC FAQ (April 23, 2025)
- **Evaluation**: 23 questions covering key regulatory topics
- **Model**: Google Gemini 2.5 Flash for production-quality answers
- **Framework**: LangChain 0.2.16 with compatible dependencies

---

## 🚨 Important for Submission

### Before Creating Video

1. Run: `python check.py` - Ensure all ✅
2. Test: `python test_working.py` - Verify RAG works
3. Practice: `python demo_faq.py` - Know the flow
4. Clear terminal: `clear` - Start with clean screen

### Before Zipping Project

1. Remove: `.venv/` directory (too large)
2. Keep: `data/index.faiss/` (essential)
3. Keep: PDF file (essential)
4. Include: `.env.example` (not `.env` with actual keys)

### Zip Command

```bash
cd /Users/venom/Downloads
zip -r proj2.zip proj2/ -x "proj2/.venv/*" "proj2/**/__pycache__/*" "proj2/.DS_Store"
```

---

## 🤝 Support

If you encounter issues:
1. Run `python check.py` for diagnostics
2. Check logs in terminal output
3. Verify API keys in `.env`
4. Ensure FAISS index exists in `data/index.faiss/`

---

**Built with ❤️ using Google Gemini, LangChain, and FAISS**
