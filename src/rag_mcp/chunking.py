import re


def chunk_by_sentences(text: str, max_chars: int = 800, overlap_sentences: int = 1) -> list[str]:
    """Split text into chunks along sentence boundaries, never mid-sentence."""
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    chunks = []
    current: list[str] = []
    current_len = 0

    for sentence in sentences:
        if current_len + len(sentence) > max_chars and current:
            chunks.append(" ".join(current))
            current = current[-overlap_sentences:] if overlap_sentences else []
            current_len = sum(len(s) for s in current)
        current.append(sentence)
        current_len += len(sentence)

    if current:
        chunks.append(" ".join(current))

    return chunks
