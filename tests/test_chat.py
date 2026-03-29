import pytest


@pytest.mark.asyncio
async def test_chat_with_fake_provider(client, fake_provider):
    response = await client.post(
        "/api/v1/chat",
        json={"provider": "fake", "prompt_key": "greeting"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["response"] == "fake response"
    assert data["provider"] == "fake"
    assert data["usage"]["total_tokens"] == 30


@pytest.mark.asyncio
async def test_chat_unknown_provider(client):
    response = await client.post(
        "/api/v1/chat",
        json={"provider": "unknown", "prompt_key": "greeting"},
    )
    assert response.status_code == 400
    assert "未対応のプロバイダ" in response.json()["detail"]


@pytest.mark.asyncio
async def test_chat_unknown_prompt_key(client, fake_provider):
    response = await client.post(
        "/api/v1/chat",
        json={"provider": "fake", "prompt_key": "nonexistent"},
    )
    assert response.status_code == 400
    assert "見つかりません" in response.json()["detail"]
