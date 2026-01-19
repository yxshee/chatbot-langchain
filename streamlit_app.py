"""Streamlit UI for the RBI NBFC Chatbot.

This file focuses on a clean, chat-first UX while keeping the underlying
Gemini + FAISS RAG pipeline unchanged.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import streamlit as st
from dotenv import load_dotenv

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.rbi_nbfc_chatbot.chains import build_rag_chain
from src.rbi_nbfc_chatbot.config import (
    GEMINI_MODEL,
    GOOGLE_API_KEY,
    PDF_PATH,
    RETRIEVAL_K,
    TEMPERATURE,
    VECTOR_STORE_PATH,
)

load_dotenv()


st.set_page_config(
    page_title="RBI NBFC Chatbot",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
<style>
  /* Layout */
  .block-container { max-width: 1200px; padding-top: 1.5rem; }
  [data-testid="stSidebar"] { border-right: 1px solid rgba(229,231,235,0.8); }

  /* Hero */
  .hero {
    background: linear-gradient(135deg, #0ea5e9 0%, #2563eb 45%, #7c3aed 100%);
    border-radius: 18px;
    padding: 22px 24px;
    color: #ffffff;
    margin-bottom: 1.25rem;
  }
  .hero h1 { margin: 0; font-size: 1.9rem; line-height: 1.2; }
  .hero p { margin: 0.35rem 0 0; opacity: 0.92; }
  .badge {
    display: inline-block;
    margin-top: 0.8rem;
    margin-right: 0.5rem;
    padding: 0.35rem 0.6rem;
    font-size: 0.85rem;
    border-radius: 999px;
    background: rgba(255,255,255,0.16);
    border: 1px solid rgba(255,255,255,0.22);
  }

  /* Cards */
  .card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 14px 16px;
  }
  .card h3 { margin: 0 0 0.4rem; font-size: 1rem; }
  .muted { color: rgba(17,24,39,0.70); font-size: 0.9rem; }

  /* Sources */
  .source {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 12px 12px;
    margin: 10px 0;
  }
  .source-meta { color: rgba(17,24,39,0.65); font-size: 0.85rem; margin-bottom: 0.4rem; }
  .source-text { font-size: 0.95rem; line-height: 1.35; }
</style>
""",
    unsafe_allow_html=True,
)


@dataclass
class UISettings:
    model_name: str
    temperature: float
    retrieval_k: int
    show_sources: bool


def _init_state() -> None:
    if "settings" not in st.session_state:
        st.session_state.settings = UISettings(
            model_name=GEMINI_MODEL,
            temperature=TEMPERATURE,
            retrieval_k=RETRIEVAL_K,
            show_sources=True,
        )
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "question_count" not in st.session_state:
        st.session_state.question_count = 0
    if "pending_question" not in st.session_state:
        st.session_state.pending_question = None
    if "bootstrapped" not in st.session_state:
        st.session_state.bootstrapped = False


@st.cache_resource(show_spinner=False)
def _get_chain(model_name: str, temperature: float, k: int):
    return build_rag_chain(model_name=model_name, temperature=temperature, k=k)


def _ensure_welcome_message() -> None:
    if st.session_state.messages:
        return
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": (
                "Ask me anything about RBI regulations for Non‑Banking Financial Companies (NBFCs).\n\n"
                "I answer using the RBI Master Direction (RAG: retrieval + grounded generation)."
            ),
            "timestamp": datetime.now().isoformat(timespec="seconds"),
        }
    )


def _format_export(messages: List[Dict[str, Any]]) -> str:
    lines: List[str] = []
    for m in messages:
        role = "You" if m.get("role") == "user" else "Assistant"
        ts = m.get("timestamp") or ""
        content = (m.get("content") or "").strip()
        lines.append(f"[{ts}] {role}:\n{content}\n")
    return "\n".join(lines).strip() + "\n"


def _ask(chain, question: str, *, show_sources: bool) -> Dict[str, Any]:
    response = chain.ask_question(question, return_sources=show_sources)
    return response


def _handle_question(chain, question: str) -> None:
    q = (question or "").strip()
    if not q:
        return

    st.session_state.messages.append(
        {
            "role": "user",
            "content": q,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
        }
    )

    with st.spinner("Searching the RBI document and drafting an answer…"):
        response = _ask(chain, q, show_sources=st.session_state.settings.show_sources)

    assistant_msg: Dict[str, Any] = {
        "role": "assistant",
        "content": response.get("answer", ""),
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }

    if st.session_state.settings.show_sources:
        assistant_msg["sources"] = response.get("sources", [])

    st.session_state.messages.append(assistant_msg)
    st.session_state.question_count += 1


_init_state()


# Sidebar
with st.sidebar:
    st.title("RBI NBFC Chatbot")
    st.caption("Gemini-powered RAG over the RBI Master Direction")

    if not GOOGLE_API_KEY:
        st.error("GOOGLE_API_KEY is missing. Add it to your .env file to chat.")
    else:
        st.success("Ready")

    st.divider()

    st.subheader("Session")
    st.write(f"Questions asked: **{st.session_state.question_count}**")
    st.write(f"Messages: **{max(len(st.session_state.messages) - 1, 0)}**")

    if st.button("Reset chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.question_count = 0
        st.session_state.pending_question = None
        st.rerun()

    if st.session_state.messages:
        st.download_button(
            label="Export chat",
            data=_format_export(st.session_state.messages),
            file_name=f"rbi_nbfc_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True,
        )

    st.divider()

    st.subheader("Model & retrieval")
    model_name = st.text_input("Model", value=st.session_state.settings.model_name)
    temperature = st.slider("Temperature", 0.0, 1.0, float(st.session_state.settings.temperature), 0.05)
    retrieval_k = st.slider("Top‑K sources", 1, 10, int(st.session_state.settings.retrieval_k), 1)
    show_sources = st.toggle("Show sources", value=bool(st.session_state.settings.show_sources))

    col_apply, col_rebuild = st.columns(2)
    with col_apply:
        apply_clicked = st.button("Apply", type="primary", use_container_width=True)
    with col_rebuild:
        rebuild_clicked = st.button("Rebuild", help="Forces a fresh chain instance", use_container_width=True)

    if apply_clicked:
        model_name_clean = (model_name or "").strip()
        st.session_state.settings = UISettings(
            model_name=model_name_clean or GEMINI_MODEL,
            temperature=float(temperature),
            retrieval_k=int(retrieval_k),
            show_sources=bool(show_sources),
        )
        st.rerun()

    if rebuild_clicked:
        _get_chain.clear()
        st.rerun()

    st.divider()

    st.subheader("Sample questions")
    sample_questions = [
        "What is a Non-Banking Financial Company (NBFC)?",
        "Can NBFCs accept demand deposits?",
        "What is the minimum Net Owned Fund requirement?",
        "What are the differences between banks and NBFCs?",
        "What is the Scale Based Regulatory Framework?",
    ]
    for q in sample_questions:
        if st.button(q, use_container_width=True):
            st.session_state.pending_question = q
            st.rerun()

    st.divider()
    st.caption(f"PDF: {PDF_PATH.name}")
    st.caption(f"Vector store: {Path(VECTOR_STORE_PATH).name}")


# Main
settings: UISettings = st.session_state.settings

st.markdown(
    f"""
<div class="hero">
  <h1>RBI NBFC Regulatory Assistant</h1>
  <p>Ask questions, get answers grounded in the RBI Master Direction, and inspect the supporting excerpts.</p>
  <span class="badge">Model: {settings.model_name}</span>
  <span class="badge">Top‑K: {settings.retrieval_k}</span>
  <span class="badge">Temperature: {settings.temperature:.2f}</span>
</div>
""",
    unsafe_allow_html=True,
)

top_left, top_mid, top_right = st.columns([1.2, 1.2, 1.6])
with top_left:
    st.markdown("<div class='card'><h3>What this is</h3><div class='muted'>A chat UI over RBI NBFC guidance using Retrieval‑Augmented Generation.</div></div>", unsafe_allow_html=True)
with top_mid:
    st.markdown("<div class='card'><h3>How it answers</h3><div class='muted'>It retrieves relevant passages from the PDF index, then drafts a grounded response.</div></div>", unsafe_allow_html=True)
with top_right:
    st.markdown(
        "<div class='card'><h3>Tips</h3><div class='muted'>Be specific (e.g., ‘Net Owned Fund’), ask one question at a time, and check sources for the exact wording.</div></div>",
        unsafe_allow_html=True,
    )


# Chain init (cached)
try:
    chain = _get_chain(settings.model_name, settings.temperature, settings.retrieval_k)
except Exception as e:
    st.error(f"Failed to initialize the chatbot: {e}")
    st.stop()


_ensure_welcome_message()


tab_chat, tab_sources, tab_about = st.tabs(["Chat", "Sources", "About"])

with tab_chat:
    for m in st.session_state.messages:
        role = m.get("role", "assistant")
        with st.chat_message(role):
            st.markdown(m.get("content", ""))

            if role == "assistant" and settings.show_sources and m.get("sources"):
                sources = m.get("sources") or []
                with st.expander(f"Show {len(sources)} source excerpt(s)"):
                    for i, s in enumerate(sources, 1):
                        page = s.get("page", "Unknown")
                        src = s.get("source", "Unknown")
                        content = (s.get("content") or "").strip()
                        snippet = content[:650] + ("…" if len(content) > 650 else "")
                        st.markdown(
                            f"""
<div class="source">
  <div class="source-meta"><b>Source {i}</b> • page: {page} • {src}</div>
  <div class="source-text">{snippet}</div>
</div>
""",
                            unsafe_allow_html=True,
                        )

    prompt = st.chat_input("Ask about NBFC regulations…")

    if st.session_state.pending_question:
        prompt = st.session_state.pending_question
        st.session_state.pending_question = None

    if prompt:
        _handle_question(chain, prompt)
        st.rerun()


with tab_sources:
    st.subheader("Most recent sources")
    last_sources: List[Dict[str, Any]] = []
    for m in reversed(st.session_state.messages):
        if m.get("role") == "assistant" and m.get("sources"):
            last_sources = m.get("sources") or []
            break

    if not settings.show_sources:
        st.info("Sources are disabled in the sidebar.")
    elif not last_sources:
        st.info("Ask a question to see the retrieved excerpts here.")
    else:
        for i, s in enumerate(last_sources, 1):
            page = s.get("page", "Unknown")
            src = s.get("source", "Unknown")
            content = (s.get("content") or "").strip()
            st.markdown(
                f"""
<div class="source">
  <div class="source-meta"><b>Source {i}</b> • page: {page} • {src}</div>
  <div class="source-text">{content}</div>
</div>
""",
                unsafe_allow_html=True,
            )


with tab_about:
    st.markdown(
        """
### What’s inside

This app answers questions using a standard RAG pipeline:

- **Retriever**: FAISS vector index built from the RBI Master Direction PDF
- **LLM**: Google Gemini via LangChain
- **Grounding**: responses are expected to stay within retrieved context

### Notes

- If you see an error about missing `GOOGLE_API_KEY`, add it to `.env` and refresh.
- For best accuracy, ask specific, regulation-shaped questions.
"""
    )

