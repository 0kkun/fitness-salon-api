from google import genai
from google.genai import types

from app.config import settings
from app.schemas.chat import ChatResponse, TokenUsage
from app.services.base import AIProvider, ai_retry


class GeminiProvider(AIProvider):
    def __init__(self) -> None:
        cfg = settings.gemini
        self.cfg = cfg
        self.client = genai.Client(api_key=cfg.api_key)

    @ai_retry
    async def chat(self, prompt: dict[str, str]) -> ChatResponse:
        cfg = self.cfg

        if cfg.is_2_5:
            thinking_config = types.ThinkingConfig(thinking_budget=cfg.thinking_budget)
        else:
            thinking_config = types.ThinkingConfig(thinking_level=cfg.thinking_level)

        response = await self.client.aio.models.generate_content(
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

        return ChatResponse(
            response=response.text,
            usage=token_usage,
            model=cfg.model,
            provider="gemini",
        )

    async def close(self) -> None:
        pass  # google-genai clientにはcloseメソッドがない
