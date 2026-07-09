import chromadb
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction
from compliance_mcp.config import settings

_ollama_ef = OllamaEmbeddingFunction(
    url=f"{settings.OLLAMA_HOST}/api/embeddings",
    model_name=settings.EMBEDDING_MODEL,
)

_client = chromadb.PersistentClient(path=settings.CHROMA_PATH)


def get_document_collection(doc_id: str):
    return _client.get_or_create_collection(
        name=f"doc_{doc_id}",
        embedding_function=_ollama_ef,
    )


def index_document(doc_id: str, chunks: list[str]) -> int:
    collection = get_document_collection(doc_id)
    existing = collection.get()
    if existing["ids"]:
        # allow clean re-check after edits
        collection.delete(ids=existing["ids"])
    ids = [f"{doc_id}-{i}" for i in range(len(chunks))]
    collection.add(documents=chunks, ids=ids)
    return len(chunks)


def query_document(doc_id: str, query: str, n_results: int = 3) -> list[dict]:
    collection = get_document_collection(doc_id)
    results = collection.query(query_texts=[query], n_results=n_results)
    return [
        {"text": d, "distance": dist}
        for d, dist in zip(results["documents"][0], results["distances"][0])
    ]
