from fastapi import APIRouter, HTTPException

from app.providers import get_provider
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.prompt_loader import load_prompt
from app.services.token_logger import log_token_usage

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    try:
        provider = get_provider(request.provider)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        prompt = load_prompt(request.prompt_key, request.variables)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    result = await provider.chat(prompt)

    log_token_usage(
        provider=request.provider,
        model=result.model,
        prompt_key=request.prompt_key,
        input_tokens=result.usage.input_tokens,
        output_tokens=result.usage.output_tokens,
        total_tokens=result.usage.total_tokens,
    )

    return result
