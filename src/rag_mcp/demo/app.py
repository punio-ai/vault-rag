from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from rag_mcp.rag import generate_answer

app = FastAPI(title="RAG Knowledge Base Demo")

app.add_middleware(
    CORSMiddleware,
    # fine for a local demo, tighten before real deployment
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    question: str


@app.post("/api/query")
def query(req: QueryRequest) -> dict:
    return generate_answer(req.question)


app.mount("/", StaticFiles(directory="src/rag_mcp/demo/static",
          html=True), name="static")
