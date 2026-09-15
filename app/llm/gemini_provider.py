from google import genai
from google.genai.errors import APIError

from app.config import settings

GEMINI_MODEL = "gemini-2.5-flash"
_client = genai.Client(api_key=settings.gemini_api_key)

def gen_answer(prompt: str) -> str:
    try:
        response = _client.models.generate_content(
            model = GEMINI_MODEL,
            contents = prompt
        )
    except APIError as e:
        raise RuntimeError(f"Gemini API error: {e}") from e
    
    if not response.text:
        raise RuntimeError(f"Gemini response is empty")
    
    return response.text