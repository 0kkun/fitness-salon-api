import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.providers import init_providers, shutdown_providers
from app.routers import chat, usage

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    init_providers()
    yield
    await shutdown_providers()


app = FastAPI(title="AI API Token Usage POC", lifespan=lifespan)

app.include_router(chat.router)
app.include_router(usage.router)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled error: %s %s", request.method, request.url.path)
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
