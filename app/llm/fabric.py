from app.llm.base import LLMProvider, EmbeddingProvider
from app.llm.gemini_provider import GeminiProvider

from functools import lru_cache

@lru_cache
def _gemini() -> GeminiProvider:
    return GeminiProvider()

def get_llm_provider() -> LLMProvider:
    return _gemini()

def get_embedding_provider() -> EmbeddingProvider:
    return _gemini()