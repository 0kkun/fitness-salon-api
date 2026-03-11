from fastapi import APIRouter, HTTPException

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.gemini_service import call_gemini
from app.services.openai_service import call_openai

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])


@router.post("/openai", response_model=ChatResponse)
def chat_openai(request: ChatRequest) -> ChatResponse:
    try:
        return call_openai(request.prompt_key, request.variables)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/gemini", response_model=ChatResponse)
def chat_gemini(request: ChatRequest) -> ChatResponse:
    try:
        return call_gemini(request.prompt_key, request.variables)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
