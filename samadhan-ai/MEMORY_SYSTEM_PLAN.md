# SAMADHAN AI - MEMORY SYSTEM IMPLEMENTATION PLAN
**Version:** 1.0  
**Date:** 2026-04-18  
**Author:** AI Assistant  

---

## 📋 EXECUTIVE SUMMARY

This document outlines a comprehensive plan to add **conversation memory** to Samadhan AI, enabling:
- Multi-turn conversations
- Follow-up questions without repeating context
- Conversation history tracking
- Context-aware responses
- Session management

**Recommended Approach:** Phased implementation starting with in-memory storage (MVP) → persistent database (Production) → advanced AI features (Future)

---

## 🎯 OBJECTIVES

### Primary Goals:
1. **Enable Multi-turn Conversations** - Users can ask follow-up questions
2. **Context Awareness** - Bot understands conversation history
3. **Session Management** - Track and manage user sessions
4. **History Display** - Show conversation history in UI
5. **Seamless UX** - Natural, ChatGPT-like experience

### Success Metrics:
- 80%+ of follow-up questions correctly understood
- <100ms overhead for context retrieval
- Session persistence across browser refreshes
- User satisfaction with multi-turn interactions

---

## 🏗️ ARCHITECTURE OPTIONS

### OPTION 1: In-Memory Storage (Recommended for MVP)
**Storage:** Python dictionary in FastAPI app  
**Duration:** 30 minutes session TTL  
**Capacity:** 1000 concurrent sessions (LRU eviction)

✅ **Pros:**
- Fast (no I/O overhead)
- Simple implementation (2 hours)
- No database setup required
- Works immediately

⚠️ **Cons:**
- Lost on app restart
- Not shared across app instances (if scaled)
- Limited by server memory

🎯 **Best For:** MVP, Demo, Single-instance deployment

---

### OPTION 2: Database-Backed Storage
**Storage:** Databricks Unity Catalog table  
**Retention:** 30 days (configurable)

✅ **Pros:**
- Persistent across restarts
- Queryable for analytics
- Scales horizontally
- Audit trail

⚠️ **Cons:**
- Slower (I/O overhead)
- Requires database setup
- More complex implementation

🎯 **Best For:** Production, Multi-user, Analytics

---

### OPTION 3: Hybrid Approach (Recommended for Production)
**Storage:** In-memory cache + Databricks table  
**Strategy:** Write-through cache, async persistence

✅ **Pros:**
- Fast reads from cache
- Persistent writes to database
- Best of both worlds
- Recoverable from restarts

⚠️ **Cons:**
- Most complex implementation
- Needs cache invalidation logic

🎯 **Best For:** Production with high performance requirements

---

## 💾 DATA MODEL

### Session Structure

```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2026-04-18T02:00:00Z",
  "last_activity": "2026-04-18T02:15:00Z",
  "user_id": null,
  "conversation_history": [
    {
      "turn_id": 1,
      "timestamp": "2026-04-18T02:00:00Z",
      "user_query": {
        "detected_language": "hi-IN",
        "regional_text": "मुझे साइबर क्राइम की शिकायत करनी है",
        "english_text": "I need to file a cyber crime complaint"
      },
      "bot_response": {
        "intents": ["legal_qa"],
        "intent_scores": {"legal_qa": 0.88},
        "legal_answer": "साइबर अपराध की शिकायत के लिए...",
        "sources": [...],
        "action_pack": "..."
      },
      "metadata": {
        "response_time_ms": 3450
      }
    },
    {
      "turn_id": 2,
      "timestamp": "2026-04-18T02:05:00Z",
      "user_query": {
        "detected_language": "hi-IN",
        "regional_text": "इसके लिए कौन से दस्तावेज चाहिए?",
        "english_text": "What documents are needed for this?",
        "context_reference": "turn_1_cyber_crime"
      },
      "bot_response": {
        "intents": ["legal_qa"],
        "legal_answer": "साइबर अपराध शिकायत के लिए...",
        "sources": [...],
        "context_aware": true
      }
    }
  ],
  "extracted_entities": {
    "topics": ["cyber_crime", "complaint_procedure"],
    "laws_mentioned": ["IT Act 2000", "Section 66C"],
    "user_situation": "filing cyber crime complaint"
  }
}
```

### Database Schema (Phase 2)

```sql
CREATE TABLE workspace.samadhan_ai.conversation_history (
    session_id STRING NOT NULL,
    turn_id INT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    detected_language STRING,
    regional_text STRING,
    english_text STRING,
    intents ARRAY<STRING>,
    legal_answer STRING,
    sources STRING,  -- JSON
    action_pack STRING,
    metadata STRING,  -- JSON
    PRIMARY KEY (session_id, turn_id)
) PARTITIONED BY (DATE(timestamp));
```

---

## 🔧 IMPLEMENTATION - PHASE 1 (MVP)

### Timeline: ~3 hours
### Goal: Basic conversation memory working

### Files to Create/Modify:

#### 1. NEW: `modules/memory_manager.py`
Complete MemoryManager class with:
- Session creation and management
- Turn tracking
- History retrieval
- Context building
- Automatic cleanup (TTL + LRU)

#### 2. UPDATE: `app.py`
New endpoints:
- `POST /api/session/new` - Create new session
- `GET /api/session/{id}/history` - Get conversation history
- `DELETE /api/session/{id}` - Delete session
- Update `POST /api/legal-query` to accept `session_id`

#### 3. UPDATE: `modules/legal_wrapper.py`
New function:
- `handle_user_query_with_context(query, language, context)`
- Enhance query with conversation context
- Mark responses as context-aware

#### 4. UPDATE: `frontend/dist/index.html`
UI changes:
- Generate/load `session_id` from localStorage
- Send `session_id` with each query
- Display conversation history
- "New Conversation" button
- Context indicator badge

### Detailed Checklist:

- [ ] **Step 1:** Create `memory_manager.py` (30 min)
  - QueryTurn dataclass
  - ConversationSession dataclass
  - MemoryManager class
  - Cleanup logic

- [ ] **Step 2:** Update `app.py` (40 min)
  - Import MemoryManager
  - Initialize global memory_manager
  - Add session endpoints
  - Update legal-query endpoint

- [ ] **Step 3:** Update `legal_wrapper.py` (20 min)
  - Add context parameter
  - Implement context enhancement
  - Return context_used flag

- [ ] **Step 4:** Update frontend (40 min)
  - Session ID management (localStorage)
  - Send session_id in requests
  - Display history sidebar
  - New conversation button

- [ ] **Step 5:** Testing (30 min)
  - Test session creation
  - Test follow-up questions
  - Test history display
  - Test session persistence

---

## 🧪 TEST SCENARIOS

### Test Case 1: Basic Follow-up
```
Turn 1: "How do I file a cyber crime complaint?"
Bot: [Explains procedure]

Turn 2: "What documents are needed?"
Expected: Bot understands "documents for cyber crime complaint"
```

### Test Case 2: Context Switch
```
Turn 1: "Tell me about cyber crime"
Turn 2: "Now tell me about divorce"
Turn 3: "What were the documents for the first topic?"
Expected: Bot recalls cyber crime context
```

### Test Case 3: Session Persistence
```
1. Create session
2. Ask 3 questions
3. Refresh browser
4. Continue conversation
Expected: History preserved, session resumed
```

---

## 🎨 USER EXPERIENCE

### Conversation Flow Example:

**User:** 🎤 "मुझे साइबर क्राइम की शिकायत करनी है"  
**Bot:** [Provides cyber crime complaint procedure]

**User:** 🎤 "इसके लिए कौन से दस्तावेज चाहिए?"  
*(What documents are needed for this?)*  
**Bot:** 🔗 *Following up on: cyber crime complaint*  
[Provides specific documents for cyber crime complaints]

**User:** 🎤 "ऑनलाइन कैसे करें?"  
*(How to do it online?)*  
**Bot:** 🔗 *Context: cyber crime complaint, documents*  
[Explains online filing process on cybercrime.gov.in]

---

## 📊 PERFORMANCE CONSIDERATIONS

### Memory Limits:
- **Max conversation length:** 50 turns per session
- **Session TTL:** 30 minutes of inactivity
- **Max concurrent sessions:** 1000 (LRU eviction)
- **Context window:** Last 3-5 turns
- **Total memory usage:** ~50MB for 1000 sessions

### Optimization:
- Lazy load history (only when needed)
- Compress old turns (summarize)
- Prune low-relevance exchanges
- Use sliding window for context

---

## 🔐 PRIVACY & SECURITY

### Considerations:
- ✅ Session IDs are UUIDs (non-sequential, non-guessable)
- ✅ No personal data stored in logs
- ✅ Auto-expire sessions after 24 hours
- ✅ Option to delete conversation history
- ✅ GDPR compliant (right to be forgotten)
- ⚠️ Consider encryption for sensitive queries (Phase 2)

---

## 📈 FUTURE ENHANCEMENTS (Phase 3)

### Advanced Features:
1. **Entity Extraction** - Identify key entities (people, laws, dates)
2. **Conversation Summarization** - Auto-summarize long conversations
3. **Smart Context Selection** - Use relevance scoring for context
4. **Conversation Branching** - Support multiple topics in one session
5. **User Profiles** - Remember preferences across sessions
6. **Conversation Export** - Download chat history as PDF/JSON

---

## 🚀 DEPLOYMENT STEPS

### Phase 1 Deployment:
1. Create all new files
2. Update existing files
3. Test locally if possible
4. Deploy to Databricks Apps
5. Verify session management works
6. Test follow-up questions end-to-end

### Rollback Plan:
- Keep old app.py as backup
- If issues arise, redeploy without memory features
- Memory is additive, won't break existing functionality

---

## 📋 DECISION SUMMARY

### Recommended Path Forward:

**NOW (Phase 1 - 3 hours):**
- ✅ Implement in-memory storage
- ✅ Basic session management
- ✅ Follow-up question support
- ✅ History display in UI

**NEXT (Phase 2 - 3 hours):**
- 📅 Add database persistence
- 📅 Analytics capabilities
- 📅 Conversation export

**FUTURE (Phase 3 - 4 hours):**
- 📅 AI-powered summarization
- 📅 Smart entity extraction
- 📅 Advanced context management

---

## ✅ READY TO PROCEED?

Once approved, implementation will proceed in this order:
1. Create `memory_manager.py`
2. Update `app.py`
3. Update `legal_wrapper.py`
4. Update frontend
5. Deploy and test

**Estimated completion:** 3 hours for Phase 1 (fully functional memory system)

---

**Questions or concerns?** Review this plan carefully before we proceed with implementation.
