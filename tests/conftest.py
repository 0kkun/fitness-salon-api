import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.providers import _registry
from app.schemas.chat import ChatResponse, TokenUsage
from app.services.base import AIProvider


class FakeProvider(AIProvider):
    """テスト用のモックProvider。"""

    async def chat(self, prompt: dict[str, str]) -> ChatResponse:
        return ChatResponse(
            response="fake response",
            usage=TokenUsage(input_tokens=10, output_tokens=20, total_tokens=30),
            model="fake-model",
            provider="fake",
        )

    async def close(self) -> None:
        pass


@pytest.fixture
def fake_provider():
    provider = FakeProvider()
    _registry["fake"] = provider
    yield provider
    _registry.pop("fake", None)


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
