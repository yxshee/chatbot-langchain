#!/usr/bin/env python
"""FastAPI Web Server for RBI NBFC Chatbot.

This is a simple wrapper around the main API server for easy execution.
The actual server implementation is in src.rbi_nbfc_chatbot.api.server
"""

import os
import sys

# Add src to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the FastAPI app from the modular structure
from src.rbi_nbfc_chatbot.api import app
from src.rbi_nbfc_chatbot.config import API_HOST, API_PORT


if __name__ == "__main__":
    import uvicorn
    
    print("=" * 70)
    print("🚀 RBI NBFC Chatbot API Demo")
    print("=" * 70)
    print(f"🌐 Starting server at http://{API_HOST}:{API_PORT}")
    print(f"📝 API Documentation: http://{API_HOST}:{API_PORT}/docs")
    print(f"📖 ReDoc: http://{API_HOST}:{API_PORT}/redoc")
    print("=" * 70)
    print("\n🧪 Test with:")
    print(f"   curl -X POST http://{API_HOST}:{API_PORT}/ask \\")
    print('     -H "Content-Type: application/json" \\')
    print('     -d \'{"question": "What is an NBFC?"}\'')
    print("\n" + "=" * 70 + "\n")
    
    uvicorn.run(app, host=API_HOST, port=API_PORT)
