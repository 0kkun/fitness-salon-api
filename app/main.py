from fastapi import FastAPI

from app.routers import chat, usage

app = FastAPI(title="AI API Token Usage POC")

app.include_router(chat.router)
app.include_router(usage.router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
