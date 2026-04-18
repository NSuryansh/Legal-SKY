"""
RAG Pipeline Module
Extracted from: Retrieval Pipeline notebook
Handles vector search, retrieval, and answer generation
"""

from typing import List, Dict
import re
from databricks.vector_search.client import VectorSearchClient
from transformers import pipeline

# Vector Search Configuration
VECTOR_SEARCH_ENDPOINT = "legal_rag_endpoint"
LEGAL_INDEX_NAME = "workspace.default.legal_docs_vector_index"
SCHEME_INDEX_NAME = "workspace.default.legal_docs_vector_index"
IPC_BNS_INDEX_NAME = "workspace.default.legal_docs_vector_index"
SUMMARY_INDEX_NAME = "workspace.default.legal_docs_vector_index"
RETURN_COLUMNS = ["chunk_id", "title", "page", "source_file", "domain", "text"]

# Initialize Vector Search Client (singleton)
_vsc = None
_legal_index = None
_scheme_index = None
_ipc_bns_index = None
_summary_index = None
_generator = None


def _init_vector_search():
    """Initialize vector search indices (called once)"""
    global _vsc, _legal_index, _scheme_index, _ipc_bns_index, _summary_index
    
    if _vsc is None:
        print("Initializing Vector Search Client...")
        _vsc = VectorSearchClient(disable_notice=True)
        
        _legal_index = _vsc.get_index(
            endpoint_name=VECTOR_SEARCH_ENDPOINT,
            index_name=LEGAL_INDEX_NAME,
        )
        
        _scheme_index = _vsc.get_index(
            endpoint_name=VECTOR_SEARCH_ENDPOINT,
            index_name=SCHEME_INDEX_NAME,
        )
        
        _ipc_bns_index = _vsc.get_index(
            endpoint_name=VECTOR_SEARCH_ENDPOINT,
            index_name=IPC_BNS_INDEX_NAME,
        )
        
        _summary_index = _vsc.get_index(
            endpoint_name=VECTOR_SEARCH_ENDPOINT,
            index_name=SUMMARY_INDEX_NAME,
        )
        
        print("Vector Search indices initialized.")
    
    return _legal_index, _scheme_index, _ipc_bns_index, _summary_index


def _init_generator():
    """Initialize text generation model (called once)"""
    global _generator
    
    if _generator is None:
        print("Loading text generation model (google/flan-t5-base)...")
        _generator = pipeline(
            "text2text-generation",
            model="google/flan-t5-base",
            device=-1  # CPU
        )
        print("Generator model loaded.")
    
    return _generator


def extract_records(vs_response) -> List[Dict]:
    """Convert Vector Search response into a list of dictionaries"""
    if hasattr(vs_response, "to_dict"):
        vs_response = vs_response.to_dict()
    
    if isinstance(vs_response, list):
        return vs_response
    
    if isinstance(vs_response, dict):
        if "data_array" in vs_response:
            return vs_response["data_array"]
        elif "result" in vs_response and "data_array" in vs_response["result"]:
            return vs_response["result"]["data_array"]
        else:
            return []
    
    return []


def build_context_block(chunks: List[Dict]) -> str:
    """Build formatted context from retrieved chunks"""
    parts = []
    for i, c in enumerate(chunks, start=1):
        header = (
            f"[{i}] {c.get('title', 'Unknown')} | "
            f"page {c.get('page', 'NA')} | "
            f"{c.get('source_file', 'NA')}"
        )
        text = c.get("text", "")
        parts.append(f"{header}\n{text}")
    return "\n\n".join(parts)


def build_prompt(query: str, chunks: List[Dict], task: str) -> str:
    """Build prompt for text generation"""
    context = build_context_block(chunks)
    
    task_map = {
        "legal_qa": "Answer the legal question using only the provided context.",
        "scheme_query": "Explain the relevant government schemes using only the provided context.",
        "ipc_bns_comparison": "Compare IPC and BNS using only the provided context.",
        "legal_summarization": "Summarize the legal text using only the provided context."
    }
    
    instruction = task_map.get(task, "Answer the question using only the provided context.")
    
    prompt = f"""{instruction}

Context:
{context}

Question: {query}

Answer:"""
    
    return prompt


def generate_grounded_answer(query: str, chunks: List[Dict], task: str) -> str:
    """Generate answer grounded in retrieved context"""
    if not chunks:
        return "I could not find enough direct evidence in the indexed documents to answer this safely."
    
    generator = _init_generator()
    prompt = build_prompt(query, chunks, task)
    
    output = generator(
        prompt,
        max_new_tokens=220,
        do_sample=False,
        temperature=0.0
    )[0]["generated_text"].strip()
    
    return output


def search_index(index, query: str, k: int = 5, use_hybrid: bool = True) -> List[Dict]:
    """Search vector index with query"""
    resp = index.similarity_search(
        query_text=query,
        columns=RETURN_COLUMNS,
        num_results=k,
        query_type="hybrid" if use_hybrid else "ann",
    )
    return extract_records(resp)


def retrieve_legal(query: str, k: int = 5) -> List[Dict]:
    """Retrieve legal documents"""
    legal_index, _, _, _ = _init_vector_search()
    return search_index(legal_index, query, k=k, use_hybrid=True)


def retrieve_scheme(query: str, k: int = 5) -> List[Dict]:
    """Retrieve government scheme documents"""
    _, scheme_index, _, _ = _init_vector_search()
    return search_index(scheme_index, query, k=k, use_hybrid=True)


def retrieve_ipc_bns(query: str, k: int = 6) -> List[Dict]:
    """Retrieve IPC/BNS comparison documents"""
    _, _, ipc_bns_index, _ = _init_vector_search()
    return search_index(ipc_bns_index, query, k=k, use_hybrid=True)


def retrieve_summary(query: str, k: int = 5) -> List[Dict]:
    """Retrieve legal summaries"""
    _, _, _, summary_index = _init_vector_search()
    return search_index(summary_index, query, k=k, use_hybrid=True)


def dedupe_sources(chunks: List[Dict]) -> List[Dict]:
    """Remove duplicate sources"""
    seen = set()
    out = []
    for c in chunks:
        key = (
            c.get("chunk_id"),
            c.get("source_file"),
            c.get("page"),
            c.get("title"),
        )
        if key not in seen:
            seen.add(key)
            out.append(c)
    return out


def build_citizen_action_pack(intents: List[str], query: str) -> str:
    """Build actionable guidance for citizens"""
    blocks = []
    
    if "legal_qa" in intents or "ipc_bns_comparison" in intents:
        blocks.append(
            "### Citizen Action Pack\n"
            "1. Preserve evidence: screenshots, documents, witnesses\n"
            "2. File FIR at nearest police station or online\n"
            "3. Consult legal aid: National Legal Services Authority (NALSA)\n"
            "4. Keep copies of all documents and receipts"
        )
    
    if "scheme_query" in intents:
        blocks.append(
            "### How to Apply for Schemes\n"
            "1. Visit nearest Common Service Center (CSC)\n"
            "2. Check eligibility on government portal\n"
            "3. Gather required documents: Aadhaar, income certificate, etc.\n"
            "4. Apply online or offline with help from officials"
        )
    
    return "\n\n".join(blocks) if blocks else ""


def legal_rag_answer(query: str) -> Dict[str, object]:
    """Generate legal QA answer"""
    chunks = retrieve_legal(query, k=5)
    answer = generate_grounded_answer(query, chunks, "legal_qa")
    return {"answer": answer, "sources": chunks}


def scheme_rag_answer(query: str) -> Dict[str, object]:
    """Generate scheme query answer"""
    chunks = retrieve_scheme(query, k=5)
    answer = generate_grounded_answer(query, chunks, "scheme_query")
    return {"answer": answer, "sources": chunks}


def ipc_bns_comparison_answer(query: str) -> Dict[str, object]:
    """Generate IPC vs BNS comparison answer"""
    chunks = retrieve_ipc_bns(query, k=6)
    answer = generate_grounded_answer(query, chunks, "ipc_bns_comparison")
    return {"answer": answer, "sources": chunks}


def legal_summarization_answer(query: str) -> Dict[str, object]:
    """Generate legal summarization answer"""
    chunks = retrieve_summary(query, k=5)
    answer = generate_grounded_answer(query, chunks, "legal_summarization")
    return {"answer": answer, "sources": chunks}


def format_final_response(answer_parts: Dict[str, str], action_pack: str, sources: List[Dict]) -> str:
    """Format the final response with all parts"""
    blocks = []
    
    if answer_parts.get("legal_qa"):
        blocks.append("## Legal Answer\n" + answer_parts["legal_qa"])
    
    if answer_parts.get("scheme_query"):
        blocks.append("## Government Schemes\n" + answer_parts["scheme_query"])
    
    if answer_parts.get("ipc_bns_comparison"):
        blocks.append("## IPC vs BNS Comparison\n" + answer_parts["ipc_bns_comparison"])
    
    if answer_parts.get("legal_summarization"):
        blocks.append("## Legal Summary\n" + answer_parts["legal_summarization"])
    
    if action_pack:
        blocks.append(action_pack)
    
    return "\n\n".join(blocks)


def run_rag_pipeline(query: str, intents: List[str]) -> Dict[str, object]:
    """
    Main RAG pipeline orchestrator
    
    Args:
        query: User query in English
        intents: List of detected intents
    
    Returns:
        dict with:
            - final_answer: Complete formatted answer
            - answer_parts: Individual answers by intent
            - sources: Retrieved source documents
            - action_pack: Actionable guidance
    """
    answer_parts = {}
    all_sources = []
    
    # Process each intent
    if "legal_qa" in intents:
        result = legal_rag_answer(query)
        answer_parts["legal_qa"] = result["answer"]
        all_sources.extend(result["sources"])
    
    if "scheme_query" in intents:
        result = scheme_rag_answer(query)
        answer_parts["scheme_query"] = result["answer"]
        all_sources.extend(result["sources"])
    
    if "ipc_bns_comparison" in intents:
        result = ipc_bns_comparison_answer(query)
        answer_parts["ipc_bns_comparison"] = result["answer"]
        all_sources.extend(result["sources"])
    
    if "legal_summarization" in intents:
        result = legal_summarization_answer(query)
        answer_parts["legal_summarization"] = result["answer"]
        all_sources.extend(result["sources"])
    
    # Deduplicate sources
    all_sources = dedupe_sources(all_sources)
    
    # Build action pack
    action_pack = build_citizen_action_pack(intents, query)
    
    # Format final response
    final_answer = format_final_response(answer_parts, action_pack, all_sources)
    
    return {
        "final_answer": final_answer,
        "answer_parts": answer_parts,
        "sources": all_sources,
        "action_pack": action_pack
    }
