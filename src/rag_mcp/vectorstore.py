import chromadb
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction
from rag_mcp.config import settings

_ollama_ef = OllamaEmbeddingFunction(
    url=f"{settings.OLLAMA_HOST}/api/embeddings",
    model_name=settings.EMBEDDING_MODEL,
)

_client = chromadb.PersistentClient(path=settings.CHROMA_PATH)

_collection = _client.get_or_create_collection(
    name="knowledge_base",
    embedding_function=_ollama_ef,
)


def add_document(text: str, source: str, doc_id: str) -> None:
    _collection.add(documents=[text], metadatas=[
                    {"source": source}], ids=[doc_id])


def add_document_batch(chunks: list[str], source: str) -> int:
    ids = [f"{source}-{i}" for i in range(len(chunks))]
    metadatas = [{"source": source, "chunk_index": i}
                 for i in range(len(chunks))]
    _collection.add(documents=chunks, metadatas=metadatas, ids=ids)
    return len(chunks)


def query_documents(query: str, n_results: int = 3) -> list[dict]:
    results = _collection.query(query_texts=[query], n_results=n_results)
    docs = results["documents"][0]
    metas = results["metadatas"][0]
    distances = results["distances"][0]
    return [
        {"text": d, "source": m.get("source", "unknown"), "distance": dist}
        for d, m, dist in zip(docs, metas, distances)
    ]
