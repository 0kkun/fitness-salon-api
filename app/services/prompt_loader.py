from pathlib import Path

import yaml

PROMPTS_PATH = Path("config/prompts.yaml")


def load_prompt(prompt_key: str, variables: dict[str, str] | None = None) -> dict[str, str]:
    """設定ファイルからプロンプトを読み込み、変数を置換して返す。"""
    with open(PROMPTS_PATH) as f:
        config = yaml.safe_load(f)

    prompts = config.get("prompts", {})
    if prompt_key not in prompts:
        raise ValueError(f"プロンプトキー '{prompt_key}' が見つかりません")

    prompt = prompts[prompt_key]
    system_msg = prompt.get("system", "")
    user_msg = prompt.get("user", "")

    if variables:
        user_msg = user_msg.format(**variables)

    return {"system": system_msg, "user": user_msg}
