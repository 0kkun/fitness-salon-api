from pydantic_settings import BaseSettings


class OpenAISettings(BaseSettings):
    api_key: str = ""
    model: str = "o3"
    reasoning_effort: str = "high"

    model_config = {"env_prefix": "OPENAI_"}


class GeminiSettings(BaseSettings):
    api_key: str = ""
    model: str = "gemini-3.1-pro-preview"
    thinking_level: str = "high"
    thinking_budget: int = -1
    temperature: float = 0.0

    @property
    def is_2_5(self) -> bool:
        return "2.5" in self.model

    model_config = {"env_prefix": "GEMINI_"}


class Settings(BaseSettings):
    openai: OpenAISettings = OpenAISettings()
    gemini: GeminiSettings = GeminiSettings()

    model_config = {"env_file": ".env"}


settings = Settings()
