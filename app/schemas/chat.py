from pydantic import BaseModel


class ChatRequest(BaseModel):
    prompt_key: str
    variables: dict[str, str] | None = None


class TokenUsage(BaseModel):
    input_tokens: int
    output_tokens: int
    total_tokens: int


class ChatResponse(BaseModel):
    response: str
    usage: TokenUsage
    model: str
    provider: str
