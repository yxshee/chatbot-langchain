"""
RBI NBFC Chatbot - Streamlit Web Application
A beautiful, interactive web interface for querying RBI NBFC regulations
"""

import streamlit as st
import sys
import os
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
from src.rbi_nbfc_chatbot.chains import build_rag_chain
from src.rbi_nbfc_chatbot.chains.rag_chain import RAGChain
from src.rbi_nbfc_chatbot.config import GEMINI_MODEL, RETRIEVAL_K
from typing import Optional

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="RBI NBFC Chatbot",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
        border-bottom: 3px solid #1f77b4;
        margin-bottom: 2rem;
    }
    .stAlert {
        border-radius: 10px;
    }
    .source-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .bot-message {
        background-color: #f5f5f5;
        border-left: 4px solid #4caf50;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'rag_chain' not in st.session_state:
    st.session_state.rag_chain = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
if 'question_count' not in st.session_state:
    st.session_state.question_count = 0

# Sidebar
with st.sidebar:
    st.markdown("# 🏦 RBI NBFC Chatbot")
    st.markdown("---")
    
    st.markdown("### 📊 Session Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Questions Asked", st.session_state.question_count)
    with col2:
        st.metric("Chat History", len(st.session_state.chat_history))
    
    st.markdown("---")
    
    st.markdown("### ⚙️ Configuration")
    st.info(f"**Model:** {GEMINI_MODEL}")
    st.info(f"**Retrieval K:** {RETRIEVAL_K} documents")
    
    st.markdown("---")
    
    st.markdown("### 💡 Sample Questions")
    sample_questions = [
        "What is a Non-Banking Financial Company (NBFC)?",
        "Can NBFCs accept demand deposits?",
        "What is the minimum Net Owned Fund requirement?",
        "What are the differences between banks and NBFCs?",
        "What is Scale Based Regulatory Framework?",
    ]
    
    for i, q in enumerate(sample_questions, 1):
        if st.button(f"📌 Question {i}", key=f"sample_{i}", help=q, use_container_width=True):
            st.session_state.sample_question = q
    
    st.markdown("---")
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History", type="secondary", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.question_count = 0
        st.rerun()
    
    # Export chat button
    if st.session_state.chat_history:
        chat_text = "\n\n".join([
            f"Q: {item['question']}\nA: {item['answer']}\nTimestamp: {item['timestamp']}\n"
            for item in st.session_state.chat_history
        ])
        st.download_button(
            label="📥 Export Chat",
            data=chat_text,
            file_name=f"rbi_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    st.markdown("---")
    st.markdown("### 📚 About")
    st.markdown("""
    This chatbot uses **RAG (Retrieval-Augmented Generation)** to answer 
    questions about RBI's Master Direction for Non-Banking Financial Companies.
    
    **Powered by:**
    - 🤖 Google Gemini AI
    - 🔍 FAISS Vector Search
    - 🦜 LangChain Framework
    """)

# Main content
st.markdown('<div class="main-header">🏦 RBI NBFC Regulatory Assistant</div>', unsafe_allow_html=True)

# Initialize RAG chain
if not st.session_state.initialized:
    with st.spinner("🔄 Initializing chatbot... This may take a moment..."):
        try:
            st.session_state.rag_chain = build_rag_chain()
            st.session_state.initialized = True
            st.success("✅ Chatbot initialized successfully!")
        except Exception as e:
            st.error(f"❌ Failed to initialize chatbot: {str(e)}")
            st.error("Please ensure:\n1. Virtual environment is activated\n2. API keys are configured in .env\n3. Vector database exists")
            st.stop()

# Welcome message
if not st.session_state.chat_history:
    st.info("""
    👋 **Welcome to the RBI NBFC Regulatory Assistant!**
    
    Ask me anything about RBI's regulations for Non-Banking Financial Companies (NBFCs).
    I can help you understand:
    - NBFC definitions and types
    - Capital requirements and norms
    - Deposit acceptance rules
    - Regulatory frameworks
    - Compliance requirements
    
    💡 **Tip:** Use the sample questions in the sidebar to get started!
    """)

# Chat interface
st.markdown("### 💬 Chat with the Assistant")

# Display chat history
for i, chat in enumerate(st.session_state.chat_history):
    # User message
    with st.container():
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>🙋 You:</strong><br>
            {chat['question']}
        </div>
        """, unsafe_allow_html=True)
    
    # Bot message
    with st.container():
        st.markdown(f"""
        <div class="chat-message bot-message">
            <strong>🤖 Assistant:</strong><br>
            {chat['answer']}
        </div>
        """, unsafe_allow_html=True)
        
        # Sources expander
        if chat.get('sources'):
            with st.expander(f"📚 View {len(chat['sources'])} Source Document(s)"):
                for idx, source in enumerate(chat['sources'], 1):
                    st.markdown(f"""
                    <div class="source-box">
                        <strong>Source {idx}:</strong><br>
                        {source['content'][:300]}...
                    </div>
                    """, unsafe_allow_html=True)

# Question input
col1, col2 = st.columns([5, 1])

with col1:
    # Check if sample question was clicked
    if 'sample_question' in st.session_state:
        question = st.text_input(
            "Ask your question:",
            value=st.session_state.sample_question,
            placeholder="Type your question here...",
            key="question_input"
        )
        del st.session_state.sample_question
    else:
        question = st.text_input(
            "Ask your question:",
            placeholder="Type your question here...",
            key="question_input"
        )

with col2:
    ask_button = st.button("🚀 Ask", type="primary", use_container_width=True)

# Process question
if ask_button and question:
    if not question.strip():
        st.warning("⚠️ Please enter a question!")
    else:
        with st.spinner("🔍 Searching RBI documents and generating answer..."):
            try:
                # Get response from RAG chain
                rag_chain = st.session_state.rag_chain
                if rag_chain is None:
                    st.error("❌ RAG chain not initialized. Please refresh the page.")
                    st.stop()
                response = rag_chain.ask_question(
                    question, 
                    return_sources=True
                )
                
                # Update session state
                st.session_state.question_count += 1
                st.session_state.chat_history.append({
                    'question': question,
                    'answer': response['answer'],
                    'sources': response.get('sources', []),
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                
                # Rerun to display new message
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error processing question: {str(e)}")
                st.error("Please try rephrasing your question or check the system logs.")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**📄 Source:** RBI Master Direction (330 pages)")
with col2:
    st.markdown("**🤖 Model:** Google Gemini 2.5 Flash")
with col3:
    st.markdown("**🔍 Vector DB:** FAISS")

st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    Built with ❤️ using Streamlit • LangChain • Google Gemini AI<br>
    Data source: Reserve Bank of India (RBI)
</div>
""", unsafe_allow_html=True)
