# Vault RAG

**A private, on-premises RAG (Retrieval-Augmented Generation) assistant — exposed as an MCP server, with a live browser demo.**

Your documents never leave your infrastructure. No OpenAI API calls, no cloud data exposure — just a local vector store, a local (or self-hosted) LLM, and grounded, source-cited answers.

---

## Why this exists

Most "AI assistant" tools route your documents through a third-party API. For businesses handling sensitive data — legal, healthcare, internal financials, client records — that's a non-starter.

Vault RAG proves a different deployment model: retrieval, embedding, and generation can all run entirely on infrastructure you control, with zero external API dependency, while still producing accurate, grounded answers instead of hallucinated ones.

This repo is both:
- A **working reference implementation** of that pattern
- An **MCP server** — meaning any MCP-compatible client (Claude Desktop, custom agents, etc.) can call its tools directly, not just the bundled demo UI

---

## How it works

```
┌─────────────┐      ┌──────────────┐      ┌───────────────┐
│   Client     │      │  Vault RAG   │      │   ChromaDB    │
│ (MCP host /  │◄────►│    Server    │◄────►│ (vector store)│
│  browser UI) │      │  (FastMCP)   │      │               │
└─────────────┘      └──────┬───────┘      └───────────────┘
                             │
                             ▼
                      ┌──────────────┐
                      │    Ollama    │
                      │ (local LLM + │
                      │  embeddings) │
                      └──────────────┘
```

1. Documents are chunked along **sentence boundaries** (not fixed character counts) to avoid splitting facts mid-sentence, with a one-sentence overlap to preserve context across chunk edges.
2. Chunks are embedded and stored in a local **ChromaDB** collection.
3. A query retrieves the top-matching chunks and filters out weak matches below a relevance threshold — irrelevant documents never make it into the prompt.
4. The LLM is instructed to answer **only from retrieved context** and to say so explicitly when the context doesn't contain the answer — this is what prevents hallucination when retrieval comes up empty.
5. Every answer returns its **source documents**, so responses are auditable, not just plausible-sounding.

---

## Tools exposed via MCP

| Tool | Description |
|---|---|
| `health_check` | Confirms the server is running and reports current model configuration |
| `ingest_file` | Chunks and embeds a document from `docs_to_ingest/` into the knowledge base |
| `search_documents` | Raw semantic search — returns matching chunks with relevance scores |
| `rag_query` | Full retrieval-augmented Q&A — grounded answer plus cited sources |

---

## Live demo

A minimal FastAPI + browser UI is included (`demo/`) so the system can be shown to a non-technical audience without any MCP client setup — just a browser.

```bash
uv run uvicorn rag_mcp.demo.app:app --reload --port 8000
```

Then open `http://localhost:8000` and ask a question about the ingested documents.

**Example:**
> **You:** What percent of the ocean floor has never been mapped?
> **Answer:** Over 80%.
> **Sources:** deep_ocean.txt

---

## Setup

```bash
# 1. Clone and install dependencies
git clone https://github.com/<your-username>/vault-rag.git
cd vault-rag
uv sync

# 2. Pull required Ollama models
ollama pull mxbai-embed-large
ollama pull llama3.2

# 3. Add .env
cp .env.example .env

# 4. Run the MCP server standalone (for MCP client testing)
uv run fastmcp dev src/rag_mcp/server.py

# 5. Or run the browser demo
uv run uvicorn demo.app:app --reload --port 8000
```

---

## Architecture notes (for engineers reviewing this repo)

- **Zero MCP imports in business logic.** `rag.py` and `vectorstore.py` have no knowledge of MCP — they're plain Python modules. The MCP layer (`server.py`) and the demo layer (`demo/app.py`) both call the same underlying functions. This means the LLM backend (currently Ollama) can be swapped for a hosted provider without touching the MCP or web layers.
- **Module-level ChromaDB client.** Instantiated once, not per-request, to avoid SQLite lock contention.
- **Deterministic chunk IDs** (`source-0`, `source-1`, ...) so re-ingesting an updated file overwrites old chunks instead of duplicating them.
- **Relevance threshold on retrieval**, not just top-k. Returning the "closest available" chunks regardless of actual relevance is a common RAG failure mode — this filters chunks above a distance cutoff before they ever reach the prompt.

---

## Roadmap

- [ ] Swap Ollama → Groq for cloud-hosted deployments (interface designed for this — see architecture notes)
- [ ] Streaming responses in the demo UI
- [ ] Multi-file drag-and-drop ingestion from the browser
- [ ] Configurable relevance threshold via environment variable

---

## License

MIT
