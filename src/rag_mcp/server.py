from rag_mcp.rag import generate_answer
from rag_mcp.vectorstore import add_document_batch
from rag_mcp.chunking import chunk_by_sentences
from pathlib import Path
from rag_mcp.vectorstore import add_document, query_documents
import uuid
from fastmcp import FastMCP
from rag_mcp.config import settings

mcp = FastMCP("rag-knowledge-server")


@mcp.tool
def health_check() -> dict:
    """Check that the RAG MCP server is alive and report current config."""
    return {
        "status": "ok",
        "ollama_host": settings.OLLAMA_HOST,
        "embedding_model": settings.EMBEDDING_MODEL,
        "llm_model": settings.LLM_MODEL,
    }


# @mcp.tool
# def ingest_document(text: str, source: str = "manual") -> dict:
#     """Add a document chunk to the knowledge base for later retrieval."""
#     doc_id = str(uuid.uuid4())
#     add_document(text=text, source=source, doc_id=doc_id)
#     return {"status": "ingested", "id": doc_id, "source": source}


@mcp.tool
def ingest_file(filename: str) -> dict:
    """Chunk and ingest a text file from docs_to_ingest/ into the knowledge base."""
    path = Path("docs_to_ingest") / filename
    if not path.exists():
        return {"status": "error", "message": f"{filename} not found in docs_to_ingest/"}

    text = path.read_text(encoding="utf-8")
    chunks = chunk_by_sentences(text)
    count = add_document_batch(chunks, source=filename)
    return {"status": "ingested", "source": filename, "chunk_count": count}


@mcp.tool
def search_documents(query: str, n_results: int = 3) -> list[dict]:
    """Search the knowledge base for chunks relevant to a query."""
    return query_documents(query, n_results=n_results)


@mcp.tool
def rag_query(question: str, n_results: int = 3) -> dict:
    """Answer a question using retrieval-augmented generation over the knowledge base."""
    return generate_answer(question, n_results=n_results)


if __name__ == "__main__":
    mcp.run()
