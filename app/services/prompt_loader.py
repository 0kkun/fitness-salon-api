from pathlib import Path

import yaml

PROMPTS_PATH = Path("config/prompts.yaml")

_cache: dict[str, dict] | None = None


def _load_config() -> dict[str, dict]:
    global _cache
    if _cache is None:
        with open(PROMPTS_PATH) as f:
            config = yaml.safe_load(f)
        _cache = config.get("prompts", {})
    return _cache


def load_prompt(prompt_key: str, variables: dict[str, str] | None = None) -> dict[str, str]:
    """キャッシュ済みのプロンプト設定から読み込み、変数を置換して返す。"""
    prompts = _load_config()

    if prompt_key not in prompts:
        raise ValueError(f"プロンプトキー '{prompt_key}' が見つかりません")

    prompt = prompts[prompt_key]
    system_msg = prompt.get("system", "")
    user_msg = prompt.get("user", "")

    if variables:
        user_msg = user_msg.format(**variables)

    return {"system": system_msg, "user": user_msg}
