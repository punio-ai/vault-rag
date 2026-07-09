import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    OLLAMA_HOST: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "mxbai-embed-large")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "llama3.2")
    CHROMA_PATH: str = os.getenv("CHROMA_PATH", "./data/chroma")


settings = Settings()
