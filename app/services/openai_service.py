from openai import OpenAI

from app.config import settings
from app.schemas.chat import ChatResponse, TokenUsage
from app.services.prompt_loader import load_prompt
from app.services.token_logger import log_token_usage


def call_openai(prompt_key: str, variables: dict[str, str] | None = None) -> ChatResponse:
    cfg = settings.openai
    client = OpenAI(api_key=cfg.api_key)
    prompt = load_prompt(prompt_key, variables)

    response = client.chat.completions.create(
        model=cfg.model,
        reasoning_effort=cfg.reasoning_effort,
        messages=[
            {"role": "developer", "content": prompt["system"]},
            {"role": "user", "content": prompt["user"]},
        ],
    )

    usage = response.usage
    token_usage = TokenUsage(
        input_tokens=usage.prompt_tokens,
        output_tokens=usage.completion_tokens,
        total_tokens=usage.total_tokens,
    )

    log_token_usage(
        provider="openai",
        model=cfg.model,
        prompt_key=prompt_key,
        input_tokens=token_usage.input_tokens,
        output_tokens=token_usage.output_tokens,
        total_tokens=token_usage.total_tokens,
    )

    return ChatResponse(
        response=response.choices[0].message.content,
        usage=token_usage,
        model=cfg.model,
        provider="openai",
    )
