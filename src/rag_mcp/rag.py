import httpx
from rag_mcp.config import settings
from rag_mcp.vectorstore import query_documents

RAG_PROMPT_TEMPLATE = """Answer the question using ONLY the context below. \
If the context doesn't contain the answer, say so explicitly — do not use outside knowledge.

Context:
{context}

Question: {question}

Answer:"""


def _build_context(chunks: list[dict]) -> str:
    return "\n\n".join(
        f"[Source: {c['source']}]\n{c['text']}" for c in chunks
    )


def generate_answer(question: str, n_results: int = 3, max_distance: float = 0.55) -> dict:
    chunks = query_documents(question, n_results=n_results)
    relevant_chunks = [c for c in chunks if c["distance"] <= max_distance]

    if not relevant_chunks:
        return {"answer": "No relevant documents found.", "sources": []}

    context = _build_context(relevant_chunks)
    prompt = RAG_PROMPT_TEMPLATE.format(context=context, question=question)

    response = httpx.post(
        f"{settings.OLLAMA_HOST}/api/generate",
        json={"model": settings.LLM_MODEL, "prompt": prompt, "stream": False},
        timeout=60.0,
    )
    response.raise_for_status()
    answer = response.json()["response"]

    return {
        "answer": answer.strip(),
        "sources": [{"source": c["source"], "distance": c["distance"]} for c in relevant_chunks],
    }
