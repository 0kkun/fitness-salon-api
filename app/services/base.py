from abc import ABC, abstractmethod

from tenacity import retry, stop_after_attempt, wait_exponential

from app.schemas.chat import ChatResponse

ai_retry = retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    reraise=True,
)


class AIProvider(ABC):
    """AI Providerの共通インターフェース。"""

    @abstractmethod
    async def chat(self, prompt: dict[str, str]) -> ChatResponse:
        """プロンプトを受け取り、ChatResponseを返す。"""

    @abstractmethod
    async def close(self) -> None:
        """クライアントリソースを解放する。"""
