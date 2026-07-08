# RAG Knowledge Base MCP Server

An MCP server exposing a local, private RAG pipeline (ChromaDB + Ollama)
as tools any MCP-compatible client can call — Claude Desktop, Cursor, etc.

## Why
Demonstrates a fully local, private RAG deployment pattern: no data
leaves the machine, no API keys required, model swappable (Ollama → Groq).

## Architecture
[one diagram or bullet list: server.py -> rag.py -> vectorstore.py -> Chroma/Ollama]

## Tools
- `ingest_file(filename)` — chunk + embed a document
- `search_documents(query, n_results)` — raw semantic search
- `rag_query(question, n_results)` — grounded Q&A with anti-hallucination guardrails

## Setup
[uv commands from Lesson 1]

## Example
[paste one real rag_query request/response, like the fermentation one above]