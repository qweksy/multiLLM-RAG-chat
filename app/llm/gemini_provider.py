from google import genai
from google.genai.errors import APIError

from app.llm.base import LLMProvider, EmbeddingProvider

from app.config import settings

GEMINI_GENERATION_MODEL = "gemini-2.5-flash"
GEMINI_EMBEDDING_MODEL = "models/text-embedding-004"

class GeminiProvider(LLMProvider, EmbeddingProvider):
    """Провайдер, который закрывает интерфейс для генерации и эмбеддинги."""
    
    def __init__(self):
        self._client = genai.Client(api_key=settings.gemini_api_key)
        
    @property
    def embedding_model_name(self):
        return GEMINI_EMBEDDING_MODEL
    
    def generate_answer(self, prompt: str) -> str:
        try:
            response = self._client.models.generate_content(
                model = GEMINI_GENERATION_MODEL,
                contents = prompt
            )
        except APIError as e:
            raise RuntimeError(f"Gemini API error: {e}") from e
            
        if not response.text:
            raise RuntimeError(f"Gemini response is empty")

        return response.text
    
    def embed_text(self, text: str) -> list[float]:
        return self.embed_batch([text])[0]
    
    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        try:
            response = self._client.models.embed_content(
                model=GEMINI_EMBEDDING_MODEL,
                contents=texts
            )
        except APIError as e:
            raise RuntimeError(f"Gemini embedding API error: {e}") from e
        
        if not response.embeddings:
            raise RuntimeError("Gemini embeggings is empty")
 
        result: list[list[float]] = []
        
        for embedding in response.embeddings:
            if embedding.values is None:
                raise RuntimeError("Gemini embedding is empty")
            result.append(embedding.values)

        return result