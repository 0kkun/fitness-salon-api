import csv
from pathlib import Path

from fastapi import APIRouter

from app.services.token_logger import FIELDNAMES, LOG_PATH

router = APIRouter(prefix="/api/v1/usage", tags=["usage"])


@router.get("/logs")
def get_usage_logs() -> dict:
    log_file = Path(LOG_PATH)
    if not log_file.exists():
        return {"logs": []}

    with open(log_file) as f:
        reader = csv.DictReader(f, fieldnames=FIELDNAMES)
        next(reader)  # skip header
        logs = []
        for row in reader:
            row["input_tokens"] = int(row["input_tokens"])
            row["output_tokens"] = int(row["output_tokens"])
            row["total_tokens"] = int(row["total_tokens"])
            logs.append(row)

    return {"logs": logs}
