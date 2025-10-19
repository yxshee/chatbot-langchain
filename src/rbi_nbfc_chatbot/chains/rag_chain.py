"""RAG Chain implementation for RBI NBFC Chatbot.

This module provides the complete Retrieval-Augmented Generation pipeline
for answering questions about RBI NBFC regulations.
"""

from typing import Dict, List, Any, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

from .retriever import create_retriever
from ..config import (
    GOOGLE_API_KEY,
    GEMINI_MODEL,
    TEMPERATURE,
    RETRIEVAL_K
)

# Default prompt template for RBI NBFC questions
DEFAULT_PROMPT_TEMPLATE = """You are an expert assistant for RBI (Reserve Bank of India) NBFC (Non-Banking Financial Company) regulations.

Use the following context from the RBI Master Direction to answer the question. If you cannot find the answer in the context, clearly state that the information is not available.

IMPORTANT GUIDELINES:
1. Answer ONLY based on the provided context
2. Include specific section/paragraph references when available
3. Be precise and cite regulatory requirements accurately
4. Use clear, professional language
5. If information is not in the context, say so clearly

Context:
{context}

Question: {question}

Answer:"""


class RAGChain:
    """
    Retrieval-Augmented Generation chain for RBI NBFC chatbot.
    
    This class wraps the LangChain RAG pipeline and provides a clean interface
    for asking questions about RBI regulations.
    """
    
    def __init__(
        self,
        model_name: Optional[str] = None,
        temperature: Optional[float] = None,
        k: Optional[int] = None,
        api_key: Optional[str] = None,
        prompt_template: Optional[str] = None
    ):
        """
        Initialize the RAG chain.
        
        Args:
            model_name: Gemini model name (default: from config)
            temperature: Model temperature (default: from config)
            k: Number of documents to retrieve (default: from config)
            api_key: Google API key (default: from config)
            prompt_template: Custom prompt template (default: built-in)
        """
        self.model_name = model_name or GEMINI_MODEL
        self.temperature = temperature if temperature is not None else TEMPERATURE
        self.k = k or RETRIEVAL_K
        self.api_key = api_key or GOOGLE_API_KEY
        
        if not self.api_key:
            raise ValueError("Google API key is required. Set GOOGLE_API_KEY in .env file")
        
        # Initialize LLM
        self.llm = ChatGoogleGenerativeAI(
            model=self.model_name,
            google_api_key=self.api_key,
            temperature=self.temperature
        )
        
        # Create retriever
        self.retriever = create_retriever(k=self.k, api_key=self.api_key)
        
        # Create prompt
        template = prompt_template or DEFAULT_PROMPT_TEMPLATE
        self.prompt = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
        
        # Create QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            chain_type_kwargs={"prompt": self.prompt},
            return_source_documents=True
        )
    
    def ask_question(self, question: str, return_sources: bool = True) -> Dict[str, Any]:
        """
        Ask a question about RBI NBFC regulations.
        
        Args:
            question: The question to ask
            return_sources: Whether to include source documents in response
        
        Returns:
            Dictionary containing:
                - answer: The generated answer
                - sources: List of source documents (if return_sources=True)
                - model: Model name used
                - question: The original question
        """
        # Query the chain
        result = self.qa_chain({"query": question})
        
        # Format response
        response = {
            "question": question,
            "answer": result.get("result", ""),
            "model": self.model_name
        }
        
        # Add sources if requested
        if return_sources:
            source_docs = result.get("source_documents", [])
            response["sources"] = [
                {
                    "content": doc.page_content,
                    "page": doc.metadata.get("page", "Unknown"),
                    "source": doc.metadata.get("source", "Unknown")
                }
                for doc in source_docs
            ]
        
        return response
    
    def ask(self, question: str) -> str:
        """
        Ask a question and return just the answer text.
        
        Args:
            question: The question to ask
        
        Returns:
            The answer as a string
        """
        response = self.ask_question(question, return_sources=False)
        return response["answer"]


def build_rag_chain(
    model_name: Optional[str] = None,
    temperature: Optional[float] = None,
    k: Optional[int] = None,
    api_key: Optional[str] = None,
    prompt_template: Optional[str] = None
) -> RAGChain:
    """
    Build and return a RAG chain instance.
    
    This is a convenience function for creating a RAG chain with default
    or custom configuration.
    
    Args:
        model_name: Gemini model name (default: from config)
        temperature: Model temperature (default: from config)
        k: Number of documents to retrieve (default: from config)
        api_key: Google API key (default: from config)
        prompt_template: Custom prompt template (default: built-in)
    
    Returns:
        RAGChain: Configured RAG chain instance
    
    Example:
        >>> from src.rbi_nbfc_chatbot.chains import build_rag_chain
        >>> rag = build_rag_chain()
        >>> response = rag.ask_question("What is an NBFC?")
        >>> print(response["answer"])
    """
    return RAGChain(
        model_name=model_name,
        temperature=temperature,
        k=k,
        api_key=api_key,
        prompt_template=prompt_template
    )
