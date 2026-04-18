"""
Intent Classification Module
Extracted from: Query Understanding notebook
Performs semantic intent classification for legal queries
"""

from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Singleton pattern for model loading
_embedding_model = None
_prototype_embeddings = None


def get_embedding_model():
    """Get or initialize the embedding model (singleton)"""
    global _embedding_model
    if _embedding_model is None:
        print("Loading embedding model (intfloat/multilingual-e5-small)...")
        _embedding_model = SentenceTransformer("intfloat/multilingual-e5-small")
        print("Embedding model loaded.")
    return _embedding_model


# Intent prototypes for classification
INTENT_PROTOTYPES = {
    "legal_qa": [
        "What law applies if I was cheated online?",
        "How do I file a complaint for fraud?",
        "What punishment exists for theft?",
        "What section of law applies to cyber crime?"
    ],
    
    "scheme_query": [
        "Which government schemes can help poor families?",
        "Am I eligible for any government welfare schemes?",
        "Is there any financial help scheme from government?",
        "Government scheme for education support"
    ],
    
    "ipc_bns_comparison": [
        "What is the difference between IPC and BNS?",
        "Compare IPC sections with BNS sections",
        "What changed from IPC to Bharatiya Nyaya Sanhita",
        "Explain BNS section 303 vs IPC 302"
    ],
    
    "legal_summarization": [
        "Summarize this legal section for me",
        "Explain this law in simple terms",
        "What does this legal document mean?",
        "Can you simplify this legal text?"
    ]
}


def _init_prototype_embeddings():
    """Precompute prototype embeddings (called once)"""
    global _prototype_embeddings
    if _prototype_embeddings is None:
        print("Precomputing prototype embeddings...")
        model = get_embedding_model()
        _prototype_embeddings = {}
        
        for intent, examples in INTENT_PROTOTYPES.items():
            formatted_ex = [f"query: {e}" for e in examples]
            embeddings = model.encode(formatted_ex, normalize_embeddings=True)
            _prototype_embeddings[intent] = embeddings
        
        print("Prototype embeddings computed.")
    
    return _prototype_embeddings


def sementic_intent_classification(query, threshold=0.45):
    """
    Classify the intent of a legal query using semantic similarity
    
    Args:
        query: User query string
        threshold: Minimum similarity score to consider an intent (default: 0.45)
    
    Returns:
        dict with:
            - intents: List of detected intents
            - scores: Dict of intent -> confidence score
    """
    # Initialize model and prototypes
    model = get_embedding_model()
    prototype_embeddings = _init_prototype_embeddings()
    
    # Encode query
    formatted_query = f"query: {query}"
    query_embedding = model.encode(formatted_query, normalize_embeddings=True).reshape(1, -1)
    
    # Compute similarity with each intent
    intent_scores = {}
    for intent, prototypes in prototype_embeddings.items():
        cosine_similarities = cosine_similarity(query_embedding, prototypes)[0]
        intent_scores[intent] = float(np.max(cosine_similarities))
    
    # Sort by score and filter by threshold
    sorted_scores = sorted(intent_scores.items(), key=lambda x: x[1], reverse=True)
    detected_intents = [
        intent for intent, score in sorted_scores if score >= threshold
    ]
    
    # If no intents detected, use the top one
    if not detected_intents and sorted_scores:
        detected_intents = [sorted_scores[0][0]]
    
    return {
        "intents": detected_intents,
        "scores": intent_scores
    }
