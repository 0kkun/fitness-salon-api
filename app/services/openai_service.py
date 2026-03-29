from openai import AsyncOpenAI

from app.config import settings
from app.schemas.chat import ChatResponse, TokenUsage
from app.services.base import AIProvider, ai_retry


class OpenAIProvider(AIProvider):
    def __init__(self) -> None:
        cfg = settings.openai
        self.cfg = cfg
        self.client = AsyncOpenAI(api_key=cfg.api_key)

    @ai_retry
    async def chat(self, prompt: dict[str, str]) -> ChatResponse:
        cfg = self.cfg
        response = await self.client.chat.completions.create(
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

        return ChatResponse(
            response=response.choices[0].message.content,
            usage=token_usage,
            model=cfg.model,
            provider="openai",
        )

    async def close(self) -> None:
        await self.client.close()
