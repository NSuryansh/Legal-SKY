"""
Intent Classification Module - Simplified Version
Uses keyword-based classification instead of ML models
Works without heavy dependencies in Databricks Apps
"""

from typing import List, Dict

# Intent keywords mapping
INTENT_KEYWORDS = {
    "legal_qa": [
        "law", "legal", "section", "act", "crime", "punishment", "fir", "complaint",
        "कानून", "धारा", "अपराध", "सजा", "शिकायत", "एफआईआर",
        "what", "how", "why", "which", "when",
        "क्या", "कैसे", "क्यों", "कब", "कहां",
        "ipc", "bns", "court", "judge", "lawyer", "police",
        "न्यायालय", "वकील", "पुलिस", "न्यायाधीश"
    ],
    
    "scheme_query": [
        "scheme", "yojana", "योजना", "government", "सरकारी", "benefit", "लाभ",
        "apply", "आवेदन", "eligible", "पात्र", "subsidy", "सब्सिडी",
        "pmay", "ayushman", "mudra", "jan dhan", "pension",
        "help", "सहायता", "support", "assistance"
    ],
    
    "ipc_bns_comparison": [
        "difference", "अंतर", "compare", "comparison", "तुलना",
        "ipc vs bns", "bns vs ipc", "old law", "new law",
        "changed", "बदला", "replaced", "प्रतिस्थापित",
        "bharatiya nyaya sanhita", "भारतीय न्याय संहिता"
    ],
    
    "legal_summarization": [
        "summarize", "summary", "सारांश", "explain", "समझाएं",
        "simple", "सरल", "easy", "आसान", "meaning", "अर्थ",
        "what does this mean", "इसका क्या मतलब है",
        "in simple terms", "सरल भाषा में"
    ]
}

def sementic_intent_classification(query: str, threshold: float = 0.45) -> Dict:
    """
    Classify the intent of a legal query using keyword matching
    
    Args:
        query: User query string
        threshold: Not used in keyword matching (kept for compatibility)
    
    Returns:
        dict with:
            - intents: List of detected intents
            - scores: Dict of intent -> confidence score
    """
    query_lower = query.lower()
    
    # Count keyword matches for each intent with better scoring
    intent_scores = {}
    for intent, keywords in INTENT_KEYWORDS.items():
        matches = sum(1 for kw in keywords if kw.lower() in query_lower)
        # Better scoring: give meaningful scores (0-1 scale)
        # - More matches = higher score
        # - Use sqrt to make scores more distributed
        if matches > 0:
            # Score increases with matches, capped at 1.0
            # Formula: min(matches * 0.15, 1.0) for better distribution
            score = min(matches * 0.15, 1.0)
        else:
            score = 0.0
        intent_scores[intent] = float(score)
    
    # Get intents with non-zero scores
    detected_intents = [
        intent for intent, score in intent_scores.items() if score > 0
    ]
    
    # If no intents detected, default to legal_qa
    if not detected_intents:
        detected_intents = ["legal_qa"]
        intent_scores["legal_qa"] = 0.5
    
    print(f"🧠 Intent classification:")
    for intent in detected_intents:
        print(f"   - {intent}: {intent_scores[intent]:.3f}")
    
    return {
        "intents": detected_intents,
        "scores": intent_scores
    }
