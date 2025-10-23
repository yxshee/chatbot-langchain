"""LangSmith evaluation for RBI NBFC Chatbot."""

from typing import Any, Dict, Optional

from langsmith import Client
from langsmith.evaluation import evaluate

from ..chains import build_rag_chain
from ..config import LANGSMITH_API_KEY


def run_evaluation(
    dataset_name: str,
    experiment_name: Optional[str] = None,
    api_key: Optional[str] = None
) -> Any:
    """
    Run evaluation on a dataset using LangSmith.
    
    Args:
        dataset_name: Name of the dataset in LangSmith
        experiment_name: Name for this experiment (optional)
        api_key: LangSmith API key (default: from config)
    
    Returns:
        Evaluation results dictionary
    """
    api_key = api_key or LANGSMITH_API_KEY

    if not api_key:
        raise ValueError("LangSmith API key is required. Set LANGSMITH_API_KEY in .env file")

    # Initialize client
    client = Client(api_key=api_key)

    # Build RAG chain
    rag_chain = build_rag_chain()

    def predict(inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Prediction function for evaluation."""
        question = inputs.get("question", "")
        response = rag_chain.ask_question(question, return_sources=False)
        return {"answer": response["answer"]}

    # Run evaluation
    results = evaluate(
        predict,
        data=dataset_name,
        experiment_prefix=experiment_name,
        client=client
    )

    return results


if __name__ == "__main__":
    """Run evaluation as standalone script."""
    import sys

    try:
        results = run_evaluation("rbi-nbfc-faq")
        print("✅ Evaluation complete!")
        print(results)
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
