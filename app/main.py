from fastapi import Body, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.config import settings

from app.llm.fabric import get_llm_provider, get_embedding_provider

app = FastAPI(title="project-R")

app.add_middleware(
    CORSMiddleware,
    allow_origins = settings.cors_origins,
    allow_credentials = True,
    allow_headers=["*"],
    allow_methods=["*"]
)

class ChatResponse(BaseModel):
    answer: str

@app.get("/health")
def health() -> dict:
    return {"status":"ok"}

@app.post("/chat", response_model=ChatResponse)
def chat(prompt: str = Body(embed=True)) -> ChatResponse:
    try:
        answer = get_llm_provider().generate_answer(prompt=prompt)
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e
    return ChatResponse(answer=answer)

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)