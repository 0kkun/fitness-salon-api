from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    prompt_key: str = Field(
        description="config/prompts.yaml に定義されたプロンプトのキー名 (例: greeting, cost_estimation)",
    )
    variables: dict[str, str] | None = Field(
        default=None,
        description="プロンプト内の {変数名} を置換するキーバリュー (例: {\"data\": \"体重70kg\"})",
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
