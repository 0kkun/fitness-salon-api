import pytest

from app.services.prompt_loader import load_prompt


def test_load_prompt_greeting():
    prompt = load_prompt("greeting")
    assert "system" in prompt
    assert "user" in prompt
    assert len(prompt["system"]) > 0


def test_load_prompt_with_variables():
    prompt = load_prompt("cost_estimation", {"data": "体重70kg"})
    assert "体重70kg" in prompt["user"]


def test_load_prompt_unknown_key():
    with pytest.raises(ValueError, match="見つかりません"):
        load_prompt("nonexistent_key")
