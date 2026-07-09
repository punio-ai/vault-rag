from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
from compliance_mcp.chunking import chunk_by_sentences
from compliance_mcp.vectorstore import index_document
from compliance_mcp.checker import check_document

app = FastAPI(title="Compliance Checker Demo")


class CheckRequest(BaseModel):
    filename: str
    ruleset_name: str = "data_privacy_basics"


@app.post("/api/check")
def check(req: CheckRequest) -> dict:
    path = Path("docs_to_check") / req.filename
    if not path.exists():
        return {"status": "error", "message": f"{req.filename} not found"}

    text = path.read_text(encoding="utf-8")
    chunks = chunk_by_sentences(text)
    doc_id = req.filename.replace(".", "_")
    index_document(doc_id, chunks)

    return check_document(doc_id, req.ruleset_name)


app.mount("/", StaticFiles(directory="src/compliance_mcp/demo/static",
          html=True), name="static")
