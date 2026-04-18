from intent_classifier import sementic_intent_classification
from rag_pipeline import run_rag_pipeline
from sarvam_translation import translate_rag_output

def handle_user_query(query: str, original_language: str = "en-IN", conversation_history: list = None, case_summary: str = "") -> dict:
    """
    Complete legal query processing pipeline
    
    Args:
        query: User query in English
        original_language: Original language code for translation (e.g., "hi-IN", "bn-IN")
        conversation_history: List of previous user queries (for context)
        case_summary: Summary of the ongoing legal case (for context)
    
    Returns:
        dict containing:
            - status: "success" or "error"
            - query: The input query
            - original_language: Language code
            - intents: List of detected intents
            - intent_scores: Confidence scores for each intent
            - answer_parts: Individual answers by intent type
            - sources: Retrieved source documents with metadata
            - action_pack: Actionable guidance for citizens
            - final_answer: Complete answer in original language
    
    Example:
        >>> result = handle_user_query(
        ...     query="How do I file a cyber crime complaint?",
        ...     original_language="hi-IN"
        ... )
        >>> print(result["final_answer"])  # Answer in Hindi
    """
    
    # Validate input
    if query is None or not str(query).strip():
        return {
            "status": "error",
            "message": "Empty query received",
            "final_answer": "",
            "intents": [],
            "sources": [],
        }
    
    query = str(query).strip()
    
    try:
        # Step 1: Classify intent
        print(f"Step 1: Classifying intent for query: {query[:50]}...")
        intent_result = sementic_intent_classification(query)
        intents = intent_result["intents"]
        print(f"   Detected intents: {intents}")
        
        # Step 2: Run RAG pipeline
        print(f"Step 2: Running RAG pipeline...")
        rag_result = run_rag_pipeline(query, intents)
        final_answer_en = rag_result["final_answer"]
        print(f"   Generated answer ({len(final_answer_en)} chars)")
        
        # Step 3: Translate back to original language
        if original_language and original_language != "en-IN" and not original_language.startswith("en"):
            print(f"Step 3: Translating to {original_language}...")
            final_answer = translate_rag_output(
                final_answer_en, 
                target_language=original_language
            )
            print(f"   Translated answer ({len(final_answer)} chars)")
        else:
            final_answer = final_answer_en
        
        # Return complete result
        return {
            "status": "success",
            "query": query,
            "original_language": original_language,
            "intents": intents,
            "intent_scores": intent_result.get("scores", {}),
            "answer_parts": rag_result.get("answer_parts", {}),
            "sources": rag_result.get("sources", []),
            "action_pack": rag_result.get("action_pack", ""),
            "final_answer": final_answer,
        }
    
    except Exception as e:
        print(f"Error in handle_user_query: {e}")
        import traceback
        traceback.print_exc()
        
        return {
            "status": "error",
            "message": str(e),
            "query": query,
            "original_language": original_language,
            "final_answer": f"An error occurred while processing your query: {str(e)}",
            "intents": [],
            "sources": [],
        }
