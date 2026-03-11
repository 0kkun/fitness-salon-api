import csv
from datetime import datetime
from pathlib import Path

LOG_PATH = Path("logs/token_usage.csv")
FIELDNAMES = [
    "timestamp",
    "provider",
    "model",
    "prompt_key",
    "input_tokens",
    "output_tokens",
    "total_tokens",
]


def log_token_usage(
    provider: str,
    model: str,
    prompt_key: str,
    input_tokens: int,
    output_tokens: int,
    total_tokens: int,
) -> None:
    """トークン使用量をCSVファイルに記録する。"""
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    file_exists = LOG_PATH.exists()

    with open(LOG_PATH, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if not file_exists:
            writer.writeheader()
        writer.writerow(
            {
                "timestamp": datetime.now().isoformat(),
                "provider": provider,
                "model": model,
                "prompt_key": prompt_key,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": total_tokens,
            }
        )
