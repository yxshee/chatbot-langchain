#!/bin/bash

# RBI NBFC Chatbot Setup Script
# This script sets up the complete environment and tests the system

set -e  # Exit on any error

echo "🚀 Setting up RBI NBFC Chatbot..."
echo "================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8+ and try again."
    exit 1
fi

print_status "Python 3 found"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    print_status "Virtual environment created"
else
    print_status "Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
print_status "Dependencies installed"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    print_warning "Please edit .env file and add your API keys:"
    print_warning "  - GOOGLE_API_KEY (get from https://ai.google.dev/gemini-api/docs/api-key)"
    print_warning "  - LANGSMITH_API_KEY (get from https://smith.langchain.com/)"
    echo ""
    echo "After adding API keys, run this script again to continue setup."
    exit 1
else
    print_status ".env file exists"
fi

# Check if API keys are set
source .env
if [ -z "$GOOGLE_API_KEY" ] || [ "$GOOGLE_API_KEY" = "your_gemini_api_key_here" ]; then
    print_error "GOOGLE_API_KEY not set in .env file"
    print_warning "Please edit .env file and add your Gemini API key"
    exit 1
fi

if [ -z "$LANGSMITH_API_KEY" ] || [ "$LANGSMITH_API_KEY" = "your_langsmith_api_key_here" ]; then
    print_error "LANGSMITH_API_KEY not set in .env file"
    print_warning "Please edit .env file and add your LangSmith API key"
    exit 1
fi

print_status "API keys configured"

# Check if PDF exists
PDF_FILE="106MDNBFCS1910202343073E3EF57A4916AA5042911CD8D562.pdf"
if [ ! -f "$PDF_FILE" ]; then
    print_error "RBI PDF file not found: $PDF_FILE"
    print_warning "Please ensure the PDF file is in the project root directory"
    exit 1
fi

print_status "RBI PDF file found"

# Create data directory
mkdir -p data
print_status "Data directory created"

# Run PDF ingestion
echo ""
echo "🔄 Running PDF ingestion pipeline..."
echo "===================================="
python -m src.utils.ingest --is-local --log-level INFO

if [ $? -eq 0 ]; then
    print_status "PDF ingestion completed successfully"
else
    print_error "PDF ingestion failed"
    exit 1
fi

# Test the retriever
echo ""
echo "🧪 Testing retriever..."
echo "======================="
python -c "
from src.chains.retriever import RBIRetriever
from src.utils.io_helpers import setup_logging

setup_logging('INFO')
try:
    retriever = RBIRetriever()
    info = retriever.get_vector_store_info()
    print(f'Vector store loaded: {info.get(\"index_loaded\", False)}')
    print(f'Number of vectors: {info.get(\"num_vectors\", \"unknown\")}')
    
    if info.get('index_loaded'):
        results = retriever.search_similar_documents('What is an NBFC?', k=1)
        print(f'Test search returned {len(results)} results')
        print('✅ Retriever test passed')
    else:
        print('❌ Retriever test failed - index not loaded')
        exit(1)
except Exception as e:
    print(f'❌ Retriever test failed: {e}')
    exit(1)
"

if [ $? -eq 0 ]; then
    print_status "Retriever test passed"
else
    print_error "Retriever test failed"
    exit 1
fi

# Test the RAG chain
echo ""
echo "🧪 Testing RAG chain..."
echo "======================="
python -c "
from src.chains.rag_chain import build_rag_chain
from src.utils.io_helpers import setup_logging

setup_logging('INFO')
try:
    rag_chain = build_rag_chain()
    
    # Test context retrieval
    context = rag_chain.get_relevant_context('What is an NBFC?', k=2)
    print(f'Context retrieval returned {len(context)} documents')
    
    # Test full Q&A
    response = rag_chain.ask_question('What is an NBFC?')
    if 'error' not in response and response.get('answer'):
        print('✅ RAG chain test passed')
        print(f'Sample answer: {response[\"answer\"][:100]}...')
    else:
        print('❌ RAG chain test failed - no valid answer')
        exit(1)
except Exception as e:
    print(f'❌ RAG chain test failed: {e}')
    exit(1)
"

if [ $? -eq 0 ]; then
    print_status "RAG chain test passed"
else
    print_error "RAG chain test failed"
    exit 1
fi

# Create evaluation dataset
echo ""
echo "📊 Creating evaluation dataset..."
echo "================================="
python -m src.evals.build_dataset_from_rbi_faq --limit 10 --log-level INFO

if [ $? -eq 0 ]; then
    print_status "Evaluation dataset created"
else
    print_warning "Evaluation dataset creation failed (this is optional)"
fi

# Success message
echo ""
echo "🎉 Setup completed successfully!"
echo "================================"
echo ""
echo "Next steps:"
echo "1. Start the API server:"
echo "   uvicorn src.app:app --reload --port 8000"
echo ""
echo "2. Test the API:"
echo "   curl -X POST http://localhost:8000/ask \\"
echo "     -H \"Content-Type: application/json\" \\"
echo "     -d '{\"question\":\"What is an NBFC?\"}'"
echo ""
echo "3. Run evaluations:"
echo "   python -m src.evals.run_eval --dataset rbi_nbfc_faq_subset"
echo ""
echo "4. Access API documentation at:"
echo "   http://localhost:8000/docs"
echo ""
print_status "Setup complete! 🚀"