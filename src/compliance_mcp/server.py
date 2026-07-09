from compliance_mcp.checker import check_document
from pathlib import Path
from fastmcp import FastMCP
from compliance_mcp.config import settings
from compliance_mcp.chunking import chunk_by_sentences
from compliance_mcp.vectorstore import index_document
from compliance_mcp.rulesets import RULESETS

mcp = FastMCP("compliance-checker")


@mcp.tool
def health_check() -> dict:
    """Confirm the server is alive and report config."""
    return {"status": "ok", "llm_model": settings.LLM_MODEL}


@mcp.tool
def list_rulesets() -> dict:
    """List available compliance rulesets and their rule count."""
    return {name: len(rules) for name, rules in RULESETS.items()}


@mcp.tool
def ingest_document_for_check(filename: str) -> dict:
    """Chunk and index a document from docs_to_check/ for compliance checking."""
    path = Path("docs_to_check") / filename
    if not path.exists():
        return {"status": "error", "message": f"{filename} not found"}

    text = path.read_text(encoding="utf-8")
    chunks = chunk_by_sentences(text)
    doc_id = filename.replace(".", "_")
    count = index_document(doc_id, chunks)
    return {"status": "indexed", "doc_id": doc_id, "chunk_count": count}


@mcp.tool
def run_compliance_check(doc_id: str, ruleset_name: str = "data_privacy_basics") -> dict:
    """Run a compliance ruleset against a previously ingested document."""
    return check_document(doc_id, ruleset_name)


if __name__ == "__main__":
    mcp.run()
