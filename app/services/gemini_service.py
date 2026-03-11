from google import genai
from google.genai import types

from app.config import settings
from app.schemas.chat import ChatResponse, TokenUsage
from app.services.prompt_loader import load_prompt
from app.services.token_logger import log_token_usage


def call_gemini(prompt_key: str, variables: dict[str, str] | None = None) -> ChatResponse:
    cfg = settings.gemini
    client = genai.Client(api_key=cfg.api_key)
    prompt = load_prompt(prompt_key, variables)

    if cfg.is_2_5:
        thinking_config = types.ThinkingConfig(thinking_budget=cfg.thinking_budget)
    else:
        thinking_config = types.ThinkingConfig(thinking_level=cfg.thinking_level)

    response = client.models.generate_content(
        model=cfg.model,
        contents=prompt["user"],
        config=types.GenerateContentConfig(
            system_instruction=prompt["system"],
            temperature=cfg.temperature,
            thinking_config=thinking_config,
        ),
    )

    usage_metadata = response.usage_metadata
    token_usage = TokenUsage(
        input_tokens=usage_metadata.prompt_token_count,
        output_tokens=usage_metadata.candidates_token_count,
        total_tokens=usage_metadata.total_token_count,
    )

    log_token_usage(
        provider="gemini",
        model=cfg.model,
        prompt_key=prompt_key,
        input_tokens=token_usage.input_tokens,
        output_tokens=token_usage.output_tokens,
        total_tokens=token_usage.total_tokens,
    )

    return ChatResponse(
        response=response.text,
        usage=token_usage,
        model=cfg.model,
        provider="gemini",
    )
