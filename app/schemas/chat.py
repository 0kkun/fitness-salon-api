from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    provider: str = Field(
        description="使用するAIプロバイダ (例: openai, gemini)",
    )
    prompt_key: str = Field(
        description="プロンプトのキー名 (例: greeting)",
    )
    variables: dict[str, str] | None = Field(
        default=None,
        description="変数置換用キーバリュー",
    )


class TokenUsage(BaseModel):
    input_tokens: int
    output_tokens: int
    total_tokens: int


class ChatResponse(BaseModel):
    response: str
    usage: TokenUsage
    model: str
    provider: str
