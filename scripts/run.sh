#!/bin/bash

# RBI NBFC Chatbot - Quick Start Script
# This script runs all tests and demonstrations

echo "🤖 RBI NBFC CHATBOT - QUICK START"
echo "=================================="
echo ""

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "📦 Activating virtual environment..."
    source .venv/bin/activate
fi

echo "✅ Virtual environment active: $(which python)"
echo ""

# Menu
echo "Choose an option:"
echo "1) Run comprehensive tests (test_working.py)"
echo "2) Run CLI demo (demo.py)"
echo "3) Run basic chatbot test (test_chatbot.py)"
echo "4) Show project status (FINAL_STATUS.md)"
echo "5) Check dependencies"
echo "6) Run all tests"
echo ""
read -p "Enter choice [1-6]: " choice

case $choice in
    1)
        echo ""
        echo "🧪 Running comprehensive tests..."
        echo "================================="
        python test_working.py
        ;;
    2)
        echo ""
        echo "🎯 Running CLI demo..."
        echo "====================="
        python demo.py
        ;;
    3)
        echo ""
        echo "🔍 Running basic tests..."
        echo "========================"
        python test_chatbot.py
        ;;
    4)
        echo ""
        cat FINAL_STATUS.md
        ;;
    5)
        echo ""
        echo "📦 Checking dependencies..."
        echo "=========================="
        pip list | grep -E "(langchain|google|faiss|fastapi)"
        echo ""
        echo "Python version: $(python --version)"
        echo "Virtual env: $VIRTUAL_ENV"
        ;;
    6)
        echo ""
        echo "🧪 Running ALL tests..."
        echo "======================"
        echo ""
        echo ">>> Test 1: Working Tests"
        python test_working.py
        echo ""
        echo ">>> Test 2: CLI Demo"
        python demo.py
        echo ""
        echo "✅ All tests complete!"
        ;;
    *)
        echo "Invalid choice"
        ;;
esac

echo ""
echo "=================================="
echo "✅ Done!"
