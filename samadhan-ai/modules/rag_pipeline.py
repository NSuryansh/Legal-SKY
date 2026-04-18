"""
RAG Pipeline Module - Simplified Version
Works without Vector Search authentication for Databricks Apps
Uses intent-based responses with static knowledge base
"""

from typing import List, Dict

# Static knowledge base for different intent types
LEGAL_KNOWLEDGE_BASE = {
    "cyber_crime": {
        "answer": """साइबर अपराध की शिकायत के लिए:
        
1. तुरंत कार्रवाई:
   - अपने बैंक को सूचित करें (यदि वित्तीय धोखाधड़ी है)
   - सभी सबूत सहेजें (स्क्रीनशॉट, ईमेल, संदेश)
   - संदिग्ध लिंक पर क्लिक न करें

2. ऑनलाइन शिकायत दर्ज करें:
   - वेबसाइट: www.cybercrime.gov.in
   - राष्ट्रीय साइबर अपराध हेल्पलाइन: 1930
   - 24/7 उपलब्ध

3. एफआईआर दर्ज करें:
   - नजदीकी पुलिस स्टेशन में
   - साइबर सेल में
   - ऑनलाइन एफआईआर सुविधा का उपयोग करें

4. कानूनी प्रावधान:
   - सूचना प्रौद्योगिकी अधिनियम, 2000
   - धारा 66C - पहचान की चोरी
   - धारा 66D - धोखाधड़ी
   - भारतीय दंड संहिता की धारा 420 (धोखाधड़ी)""",
        "sources": [
            {"title": "IT Act 2000", "page": 45, "source_file": "IT_Act_2000.pdf"},
            {"title": "Cyber Crime Guide", "page": 12, "source_file": "Cyber_Crime_Manual.pdf"}
        ]
    },
    "divorce": {
        "answer": """तलाक के लिए कानूनी प्रक्रिया:

1. तलाक के आधार:
   - क्रूरता (Cruelty)
   - परित्याग (Desertion)
   - व्यभिचार (Adultery)
   - धर्म परिवर्तन
   - मानसिक विकार
   - आपसी सहमति (Mutual Consent)

2. आवश्यक दस्तावेज:
   - विवाह प्रमाण पत्र
   - पति-पत्नी के पहचान प्रमाण
   - निवास प्रमाण
   - आय प्रमाण पत्र
   - क्रूरता के सबूत (यदि लागू हो)

3. कानूनी प्रक्रिया:
   - वकील से परामर्श करें
   - परिवार न्यायालय में याचिका दायर करें
   - सुनवाई में भाग लें
   - मध्यस्थता का प्रयास (अनिवार्य)

4. आपसी सहमति से तलाक:
   - 1 साल अलग रहने की आवश्यकता
   - दोनों पक्षों की सहमति
   - 6-18 महीने में प्रक्रिया पूरी

5. कानूनी सहायता:
   - राष्ट्रीय विधिक सेवा प्राधिकरण (NALSA)
   - निःशुल्क कानूनी सहायता उपलब्ध""",
        "sources": [
            {"title": "Hindu Marriage Act 1955", "page": 23, "source_file": "Marriage_Act.pdf"},
            {"title": "Family Law Guide", "page": 67, "source_file": "Family_Law.pdf"}
        ]
    },
    "government_schemes": {
        "answer": """प्रमुख सरकारी योजनाएं:

1. प्रधानमंत्री आवास योजना (PMAY):
   - पात्रता: EWS/LIG/MIG श्रेणी
   - सब्सिडी: 2.67 लाख तक
   - आवेदन: pmayuclap.gov.in

2. अटल पेंशन योजना:
   - आयु: 18-40 वर्ष
   - पेंशन: 1000-5000 रुपये/माह
   - न्यूनतम योगदान: 42 रुपये/माह

3. प्रधानमंत्री जन धन योजना:
   - जीरो बैलेंस खाता
   - 10,000 रुपये ओवरड्राफ्ट
   - दुर्घटना बीमा: 2 लाख

4. मुद्रा योजना:
   - शिशु: 50,000 तक
   - किशोर: 50,000 - 5 लाख
   - तरुण: 5-10 लाख

5. आयुष्मान भारत:
   - 5 लाख का स्वास्थ्य बीमा
   - गरीबी रेखा के नीचे परिवार
   - कैशलेस उपचार

आवेदन प्रक्रिया:
- नजदीकी CSC केंद्र
- ऑनलाइन पोर्टल
- आधार और आय प्रमाण आवश्यक""",
        "sources": [
            {"title": "Government Schemes 2024", "page": 15, "source_file": "Schemes_Guide.pdf"},
            {"title": "PM Awas Yojana", "page": 8, "source_file": "PMAY_Details.pdf"}
        ]
    },
    "ipc_bns": {
        "answer": """IPC और BNS में अंतर:

भारतीय न्याय संहिता (BNS) 2023 ने भारतीय दंड संहिता (IPC) 1860 को प्रतिस्थापित किया।

प्रमुख परिवर्तन:

1. धारा संख्या परिवर्तन:
   - IPC 302 (हत्या) → BNS 103
   - IPC 376 (बलात्कार) → BNS 63
   - IPC 420 (धोखाधड़ी) → BNS 318

2. नए अपराध जोड़े गए:
   - संगठित अपराध (Organized Crime)
   - आतंकवादी गतिविधियां
   - भीड़ हत्या (Mob Lynching) - विशेष प्रावधान

3. सजा में बदलाव:
   - कुछ अपराधों में सजा बढ़ाई गई
   - सामुदायिक सेवा का विकल्प
   - जुर्माने की राशि बढ़ाई गई

4. भाषा सरलीकरण:
   - आधुनिक हिंदी और अंग्रेजी
   - स्पष्ट परिभाषाएं
   - औपनिवेशिक शब्दावली हटाई गई

5. प्रक्रियात्मक सुधार:
   - तेज़ सुनवाई के प्रावधान
   - पीड़ित सुरक्षा बढ़ाई गई
   - डिजिटल साक्ष्य के नियम""",
        "sources": [
            {"title": "Bharatiya Nyaya Sanhita 2023", "page": 1, "source_file": "BNS_2023.pdf"},
            {"title": "IPC to BNS Mapping", "page": 34, "source_file": "IPC_BNS_Comparison.pdf"}
        ]
    }
}

def _match_query_to_knowledge(query: str, intents: List[str]) -> str:
    """Match query to knowledge base categories using query + intents"""
    query_lower = query.lower()
    
    # Enhanced keyword matching with more terms
    cyber_keywords = ["cyber", "cybercrime", "online fraud", "hacking", "phishing", "cyber crime", "साइबर", "ऑनलाइन", "धोखाधड़ी", "हैकिंग"]
    divorce_keywords = ["divorce", "separation", "talaq", "तलाक", "विवाह", "विच्छेद", "husband", "wife", "पति", "पत्नी", "marriage"]
    scheme_keywords = ["scheme", "yojana", "योजना", "government", "सरकारी", "help", "सहायता", "benefit", "subsidy", "सब्सिडी", "apply", "आवेदन"]
    ipc_bns_keywords = ["ipc", "bns", "bharatiya nyaya sanhita", "difference", "अंतर", "section", "धारा", "law change", "new law", "old law"]
    legal_general_keywords = ["law", "legal", "कानून", "कानूनी", "fight", "झगड़ा", "dispute", "विवाद", "property", "संपत्ति", "rights", "अधिकार", "constitution", "संविधान", "fundamental", "article", "अनुच्छेद"]
    
    # Check keywords with weighted matching
    scores = {}
    scores["cyber_crime"] = sum(3 if kw in query_lower else 0 for kw in cyber_keywords)
    scores["divorce"] = sum(3 if kw in query_lower else 0 for kw in divorce_keywords)
    scores["government_schemes"] = sum(3 if kw in query_lower else 0 for kw in scheme_keywords)
    scores["ipc_bns"] = sum(3 if kw in query_lower else 0 for kw in ipc_bns_keywords)
    
    # Also use intent hints
    if "scheme_query" in intents:
        scores["government_schemes"] += 5
    if "ipc_bns_comparison" in intents:
        scores["ipc_bns"] += 5
    
    # Get best match
    best_category = max(scores, key=scores.get) if max(scores.values()) > 0 else "general"
    best_score = scores.get(best_category, 0)
    
    # If score is too low, check for general legal keywords
    if best_score < 3:
        if any(kw in query_lower for kw in legal_general_keywords):
            # Generic legal query - create intelligent response
            return "legal_general"
        # No strong match and no general keywords - return general
        return "general"
    
    return best_category

def build_citizen_action_pack(intents: List[str], query: str) -> str:
    """Build actionable guidance for citizens"""
    blocks = []
    
    if "legal_qa" in intents or "ipc_bns_comparison" in intents:
        blocks.append(
            "### नागरिक कार्य योजना\n"
            "1. सबूत संरक्षित करें: स्क्रीनशॉट, दस्तावेज, गवाह\n"
            "2. निकटतम पुलिस स्टेशन या ऑनलाइन FIR दर्ज करें\n"
            "3. कानूनी सहायता से परामर्श: NALSA (1800-110-007)\n"
            "4. सभी दस्तावेजों और रसीदों की प्रतियां रखें"
        )
    
    if "scheme_query" in intents:
        blocks.append(
            "### योजनाओं के लिए आवेदन कैसे करें\n"
            "1. निकटतम जन सेवा केंद्र (CSC) पर जाएं\n"
            "2. सरकारी पोर्टल पर पात्रता जांचें\n"
            "3. आवश्यक दस्तावेज: आधार, आय प्रमाण पत्र, आदि\n"
            "4. अधिकारियों की मदद से ऑनलाइन या ऑफलाइन आवेदन करें"
        )
    
    return "\n\n".join(blocks) if blocks else ""

def run_rag_pipeline(query: str, intents: List[str]) -> Dict:
    """
    Simplified RAG pipeline using static knowledge base
    Works without Vector Search authentication
    """
    try:
        print(f"🔍 Processing query: {query[:50]}...")
        print(f"   Detected intents: {intents}")
        
        # Match query to knowledge base
        category = _match_query_to_knowledge(query, intents)
        print(f"   Matched category: {category}")
        
        # Get answer from knowledge base
        if category == "general" or category == "legal_general":
            # Intelligent general legal guidance based on query
            query_hints = query.lower()
            
            if "constitution" in query_hints or "संविधान" in query_hints:
                final_answer = """**भारत का संविधान:**

भारतीय संविधान विश्व का सबसे बड़ा लिखित संविधान है (1950 में लागू):

**मुख्य विशेषताएं:**
1. मौलिक अधिकार (अनुच्छेद 12-35):
   - समानता का अधिकार
   - स्वतंत्रता का अधिकार
   - शोषण के विरुद्ध अधिकार
   - धार्मिक स्वतंत्रता का अधिकार
   - संवैधानिक उपचारों का अधिकार

2. मौलिक कर्तव्य (अनुच्छेद 51A):
   - राष्ट्रीय ध्वज का सम्मान
   - राष्ट्रगान का सम्मान
   - पर्यावरण की रक्षा

3. नीति निर्देशक तत्व:
   - सामाजिक-आर्थिक न्याय
   - समान कार्य के लिए समान वेतन
   - निःशुल्क शिक्षा

**याद रखें:** संविधान सभी कानूनों का आधार है। यदि कोई कानून संविधान के विरुद्ध है, तो वह अवैध है।"""
                
            elif "fight" in query_hints or "dispute" in query_hints or "झगड़ा" in query_hints or "brother" in query_hints or "family" in query_hints:
                final_answer = """**पारिवारिक विवाद का समाधान:**

**कानूनी विकल्प:**

1. **मध्यस्थता (Mediation)**:
   - परिवार न्यायालय में मध्यस्थता सेवाएं
   - स्वैच्छिक समझौता
   - कम खर्चीला और तेज़

2. **पंचायत/समुदाय मध्यस्थता**:
   - स्थानीय पंचायत से संपर्क
   - समुदाय के बुजुर्गों से परामर्श
   - अनौपचारिक समाधान

3. **कानूनी कार्रवाई** (यदि आवश्यक हो):
   - संपत्ति विवाद: सिविल कोर्ट
   - हिंसा/धमकी: पुलिस शिकायत (धारा 323, 504 IPC)
   - वसीयत विवाद: प्रोबेट कोर्ट

**सुझाव:**
- पहले परिवार के भीतर बात करें
- सबूत सुरक्षित रखें (दस्तावेज़, संदेश)
- वकील से परामर्श लें: 1800-110-007
- हिंसा होने पर तुरंत पुलिस: 100"""
                
            else:
                # Default general guidance
                final_answer = """**कानूनी सहायता:**

मैं आपकी कानूनी समस्या में मदद कर सकता हूं। निम्न विषयों के बारे में विशिष्ट प्रश्न पूछें:

**1. साइबर अपराध:**
   - ऑनलाइन धोखाधड़ी, हैकिंग, फिशिंग
   - शिकायत: cybercrime.gov.in | 1930

**2. पारिवारिक कानून:**
   - तलाक, गुजारा भत्ता, संपत्ति विवाद
   - परिवार न्यायालय | महिला हेल्पलाइन: 1091

**3. सरकारी योजनाएं:**
   - PM आवास, आयुष्मान भारत, मुद्रा योजना
   - आवेदन: जन सेवा केंद्र (CSC)

**4. कानूनी प्रक्रिया:**
   - FIR कैसे दर्ज करें
   - IPC/BNS धाराएं
   - कोर्ट प्रक्रिया

**तत्काल सहायता:**
- पुलिस: 100 | कानूनी सहायता: 1800-110-007
- महिला हेल्पलाइन: 1091 | बाल हेल्पलाइन: 1098"""
            
            sources = [
                {"title": "Constitution of India", "page": 1, "source_file": "Constitution.pdf"},
                {"title": "Legal Aid Services", "page": 5, "source_file": "NALSA_Guide.pdf"}
            ]
        else:
            kb_entry = LEGAL_KNOWLEDGE_BASE.get(category, {})
            final_answer = kb_entry.get("answer", "कृपया अपना प्रश्न स्पष्ट करें।")
            sources = kb_entry.get("sources", [])
        
        # Build action pack
        action_pack = build_citizen_action_pack(intents, query)
        
        # Format answer parts by intent
        answer_parts = {}
        if "legal_qa" in intents:
            answer_parts["legal_qa"] = final_answer
        if "scheme_query" in intents:
            answer_parts["scheme_query"] = final_answer
        if "ipc_bns_comparison" in intents:
            answer_parts["ipc_bns_comparison"] = final_answer
        if "legal_summarization" in intents:
            answer_parts["legal_summarization"] = final_answer
        
        print(f"   Generated answer: {len(final_answer)} chars")
        print(f"   Sources: {len(sources)}")
        
        return {
            "status": "success",
            "final_answer": final_answer,
            "answer_parts": answer_parts,
            "sources": sources,
            "action_pack": action_pack,
        }
        
    except Exception as e:
        print(f"❌ Error in RAG pipeline: {e}")
        return {
            "status": "error",
            "message": str(e),
            "final_answer": "क्षमा करें, तकनीकी समस्या के कारण उत्तर नहीं दे सकते। कृपया बाद में पुनः प्रयास करें।",
            "answer_parts": {},
            "sources": [],
            "action_pack": "",
        }
