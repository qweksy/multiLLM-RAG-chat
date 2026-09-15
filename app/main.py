from fastapi import Body, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from pydantic import BaseModel

from app.llm.gemini_provider import gen_answer

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
        answer = gen_answer(prompt=prompt)
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e
    return ChatResponse(answer=answer)

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)