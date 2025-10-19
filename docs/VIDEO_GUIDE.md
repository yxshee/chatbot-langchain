# 🎥 Video Recording Guide - RBI NBFC Chatbot

**Complete step-by-step guide for creating your Loom demonstration video**

---

## 📋 Pre-Recording Checklist

### 1. Verify Project is Ready

```bash
cd /Users/venom/Downloads/proj2
python scripts/check.py
```

✅ **Expected**: All checks should pass  
❌ **If failed**: Fix issues before recording

### 2. Prepare Your Environment

- [ ] Close unnecessary applications
- [ ] Clear terminal: `clear`
- [ ] Set terminal to fullscreen or large window
- [ ] Increase font size: Cmd+Plus (easier to read in video)
- [ ] Open browser tab: http://localhost:8000/docs (for API demo)
- [ ] Have LangSmith dashboard ready: https://smith.langchain.com

### 3. Practice Run

Do a complete dry run before recording:
```bash
python examples/demo_faq.py         # Practice the flow
python examples/demo_interactive.py  # Test 2-3 questions
python examples/demo_api.py       # Make sure it starts
```

---

## 🎬 Recording Setup

### Tools Required

1. **Loom** (https://www.loom.com)
   - Free account is sufficient
   - Desktop app or Chrome extension
   - Enable camera (optional but recommended)

2. **Terminal**
   - Use iTerm2 or default Terminal
   - Font size: 14-16pt
   - Light theme recommended (better for video)

3. **Browser**
   - Chrome or Safari
   - For API documentation demo

### Recording Settings

- **Resolution**: 1080p (1920x1080)
- **Duration target**: 10-15 minutes
- **Mic**: Built-in or external (clear audio essential)
- **Camera**: Optional (face cam adds personal touch)

---

## 🎯 Video Structure (15 Minutes)

### Part 1: Introduction (2 minutes)

**Screen: Terminal**

```bash
# Show you're in the right directory
pwd
# /Users/venom/Downloads/proj2

# Show project files
ls -la

# Show status check
python scripts/check.py
```

**What to say**:
```
"Hello! I'm going to demonstrate my RBI NBFC Chatbot, a RAG-based 
intelligent assistant for regulatory queries.

This project uses Google Gemini 2.5 Flash and LangChain to answer 
questions about RBI NBFC regulations from a 330-page Master Direction 
document.

Let me show you that everything is working properly..."

[Run check.py]

"Great! All components are ready. The system has:
- Google Gemini API connected
- FAISS vector store with 716 document chunks
- Multiple interfaces: CLI, web API, and evaluation system
- LangSmith integration for evaluation

Now let me walk you through each component..."
```

---

### Part 2: Component Explanation (4 minutes)

**Show each component file in terminal/editor**

#### Component 1: PDF Ingestion

**Screen: Show `src/utils/ingest.py` briefly**

```bash
# Just show the file exists
cat src/utils/ingest.py | head -20
```

**What to say**:
```
"First, the PDF ingestion component. This script:

1. Loads the 330-page RBI NBFC Master Direction PDF
2. Uses PyPDF to extract text from each page
3. Splits the text into 716 chunks using RecursiveCharacterTextSplitter
   - Chunk size: 1000 characters
   - Overlap: 200 characters (to maintain context)
4. Generates embeddings using Google's text-embedding-004 model
   - Creates 768-dimensional vectors for each chunk
5. Stores everything in a FAISS vector database

The result is a searchable knowledge base that we can query 
efficiently using vector similarity search."
```

#### Component 2: FAISS Retriever

**Screen: Show `src/chains/retriever.py` briefly**

```bash
cat src/chains/retriever.py | head -30
```

**What to say**:
```
"Next, the retriever component. This:

1. Loads the FAISS vector store from disk
2. Configures search to return k=4 most similar documents
3. Uses cosine similarity for ranking
4. Returns documents with metadata (page numbers, source info)

When you ask a question, this component finds the 4 most relevant 
chunks from our 716 total chunks in milliseconds."
```

#### Component 3: RAG Chain

**Screen: Show `src/chains/rag_chain.py` briefly**

```bash
cat src/chains/rag_chain.py | head -40
```

**What to say**:
```
"This is the heart of the system - the RAG chain. It:

1. Takes your question
2. Uses the retriever to find relevant context
3. Combines context with a custom prompt template
4. Sends everything to Google Gemini 2.5 Flash
5. Temperature is set to 0.1 for consistent, deterministic answers
6. Returns the answer with source citations

The prompt template specifically instructs the model to:
- Answer only from provided context
- Include section references
- State clearly when information isn't available
- Use professional, compliance-appropriate language

This ensures accuracy and prevents hallucinations."
```

#### Component 4: Evaluation System

**Screen: Show `src/evals/` directory**

```bash
ls -la src/evals/
```

**What to say**:
```
"Finally, the evaluation system. It includes:

1. build_dataset_from_rbi_faq.py: Creates a dataset with 23 FAQ 
   questions from the official RBI FAQ document dated April 23, 2025

2. run_eval.py: Runs the chatbot on all questions and evaluates with 
   four metrics:
   - Correctness: Does the answer match the reference?
   - Faithfulness: Is the answer grounded in retrieved documents?
   - Relevancy: Does the answer address the question?
   - Conciseness: Is the answer appropriately detailed?

Results are tracked in LangSmith for comprehensive analysis."
```

---

### Part 3: Live Demonstrations (6 minutes)

#### Demo 1: FAQ Demonstration (2.5 minutes)

**Screen: Terminal**

```bash
clear
python examples/demo_faq.py
```

**What to say**:
```
"Let me demonstrate with actual questions from the RBI FAQ.
I'll run through a few examples to show you how it works..."

[Wait for initialization]

"The system is initializing:
- Loading the FAISS vector store
- Connecting to Google Gemini
- Setting up the RAG pipeline

Now it's ready! Let's see the first question..."

[Show 2-3 questions, press Enter between them]

[For each question, point out]:
"Notice how it:
1. Shows the question clearly
2. Retrieves 4 relevant source documents
3. Generates an accurate answer
4. Provides source citations with page numbers

The answer is comprehensive, accurate, and includes specific 
regulatory details from the Master Direction."
```

#### Demo 2: Interactive Chatbot (2 minutes)

**Screen: Terminal**

```bash
clear
python examples/demo_interactive.py
```

**What to say**:
```
"Now let me show you the interactive mode. This is perfect for 
exploratory research or compliance questions on the fly."

[Ask 2-3 questions]

Example questions:
1. "What are the licensing requirements for different NBFC categories?"
2. "Explain the Asset Liability Management framework"
3. "What are the corporate governance requirements?"

[For each answer, say]:
"The chatbot understands the question, retrieves relevant context,
and provides a detailed regulatory answer with proper citations.

This would be extremely useful for:
- Compliance officers researching regulations
- NBFC operators understanding requirements
- Financial analysts studying the regulatory framework"

[Exit gracefully]
"I can exit anytime by typing 'exit' or pressing Ctrl+C."
```

#### Demo 3: Web API (1.5 minutes)

**Screen: Split - Terminal + Browser**

```bash
# Terminal
clear
python examples/demo_api.py
```

**Browser**: Navigate to http://localhost:8000/docs

**What to say**:
```
"For production use, I've also created a RESTful API using FastAPI.

[Show terminal starting]
"The API server is now running on port 8000..."

[Switch to browser]
"Here's the Swagger UI - automatic interactive documentation.

The API has a POST /ask endpoint that accepts JSON with a question
and returns JSON with the answer and sources.

Let me test it..."

[In Swagger UI]:
1. Click "Try it out"
2. Enter question: "What is the minimum capital requirement for NBFCs?"
3. Click "Execute"

[Show response]
"The API returns a structured JSON response with:
- The original question
- The generated answer
- Source documents with page numbers
- Model information

This makes it easy to integrate the chatbot into:
- Web applications
- Mobile apps
- Internal compliance systems
- Automated workflows"
```

**Stop the server**: Ctrl+C in terminal

---

### Part 4: Evaluation System (2 minutes)

**Screen: Terminal**

```bash
clear

# Create a small test dataset
python -m src.evals.build_dataset_from_rbi_faq --limit 3 --dataset-name "Video-Demo"
```

**What to say**:
```
"Now let me demonstrate the evaluation system.

I'm creating a LangSmith dataset with 3 questions from the official 
RBI FAQ for this demo. In production, I have 23 questions.

[Wait for creation]

"The dataset is created in LangSmith. Each entry has:
- The question
- The expected reference answer from the official FAQ

Now let's run the evaluation..."
```

```bash
# Run evaluation
python -m src.evals.run_eval --dataset "Video-Demo" --experiment-name "video-demo"
```

**What to say**:
```
"The evaluation runner is now:
1. Asking each question to the chatbot
2. Collecting the generated answers
3. Computing four metrics for each response

[Wait for completion]

"Evaluation complete! The results are now in LangSmith.

Let me show you the dashboard..."
```

**Screen: Browser - LangSmith Dashboard**

```
[Open https://smith.langchain.com]

"In the LangSmith dashboard, you can see:
- All evaluated questions
- Generated answers vs expected answers
- Scores for each metric:
  * Correctness
  * Faithfulness
  * Relevancy
  * Conciseness
- Experiment history and comparisons

This makes it easy to:
- Track chatbot performance over time
- Identify areas for improvement
- Ensure regulatory accuracy
- Monitor for any degradation"
```

---

### Part 5: Wrap-up (1 minute)

**Screen: Terminal**

```bash
clear
python scripts/check.py
```

**What to say**:
```
"Let me do a final status check...

[Show check.py output]

"Perfect! All components are working:
✅ Environment configured
✅ Data files present
✅ All dependencies installed
✅ Core components ready
✅ Evaluation system operational

To summarize, this project demonstrates:

1. Complete RAG pipeline using Google Gemini and LangChain
2. Production-ready code with error handling
3. Multiple interfaces: CLI, interactive, and web API
4. Comprehensive evaluation framework with LangSmith
5. Accurate answers from a 330-page regulatory document

The system processes 716 document chunks, uses vector similarity 
search for retrieval, and generates precise answers with source 
citations.

Key technologies:
- Google Gemini 2.5 Flash for LLM
- Google text-embedding-004 for embeddings
- FAISS for vector storage
- LangChain for RAG orchestration
- FastAPI for web interface
- LangSmith for evaluation

Thank you for watching!"
```

---

## ⚙️ Technical Tips for Recording

### Terminal Appearance

```bash
# Make terminal look good
export PS1='$ '  # Simple prompt

# Increase font size
# Cmd+Plus (or Ctrl+Plus)

# Use light theme for better visibility
```

### If Something Goes Wrong During Recording

**DON'T PANIC!** Just:
1. Pause recording (if possible)
2. Fix the issue
3. Resume and say: "Let me try that again..."
4. OR: Stop, fix, and re-record that section

### Common Issues and Solutions

**Issue**: Model takes too long to respond  
**Solution**: Say "Let me give it a moment to process..." (normal)

**Issue**: Forgot what to say next  
**Solution**: Have this guide open in a second screen/device

**Issue**: Error appears  
**Solution**: "Looks like we hit an error. Let me fix that..." (show debugging if quick)

---

## 📝 Script Cheat Sheet

### Opening Line
```
"Hello! I'm demonstrating my RBI NBFC Chatbot, a RAG-based system 
for answering regulatory questions using Google Gemini and LangChain."
```

### Transition Phrases
- "Let me show you..."
- "Now let's look at..."
- "This is interesting because..."
- "Notice how..."
- "As you can see..."

### Closing Line
```
"Thank you for watching this demonstration of a production-ready 
RAG system for RBI NBFC regulatory queries!"
```

---

## ✅ Post-Recording Checklist

- [ ] Video is 10-15 minutes
- [ ] Audio is clear
- [ ] All demos worked successfully
- [ ] Explained all 4 components
- [ ] Showed interactive, API, and evaluation
- [ ] Mentioned Google Gemini and LangChain
- [ ] Video uploaded to Loom/YouTube
- [ ] Video link saved for submission

---

## 🎯 Key Points to Emphasize

1. **Technology Stack**: Google Gemini 2.5 Flash + LangChain + FAISS
2. **Scale**: 330-page PDF → 716 chunks
3. **Accuracy**: Source citations + evaluation metrics
4. **Production-Ready**: Error handling, logging, multiple interfaces
5. **Evaluation**: LangSmith integration with 4 metrics
6. **Real-World Use**: Compliance queries, regulatory research

---

## 💡 Video Recording Best Practices

### Do:
✅ Speak clearly and at moderate pace  
✅ Explain as you demonstrate  
✅ Highlight key technical details  
✅ Show real output and responses  
✅ Be enthusiastic about your project  

### Don't:
❌ Rush through demonstrations  
❌ Skip explaining components  
❌ Use jargon without explanation  
❌ Show irrelevant errors  
❌ Make it too long (>20 min)  

---

## 🎬 Final Recording Commands Reference

```bash
# Quick reference for video

# 1. Status check
python scripts/check.py

# 2. FAQ demo (show 2-3 questions)
python examples/demo_faq.py

# 3. Interactive chatbot
python examples/demo_interactive.py

# 4. API server
python examples/demo_api.py
# Then visit: http://localhost:8000/docs

# 5. Create eval dataset
python -m src.evals.build_dataset_from_rbi_faq --limit 3 --dataset-name "Video-Demo"

# 6. Run evaluation
python -m src.evals.run_eval --dataset "Video-Demo" --experiment-name "video-demo"

# 7. Final status check
python scripts/check.py
```

---

**Good luck with your recording! 🎥 You've got this! 🚀**
