from app.services.base import AIProvider
from app.services.gemini_service import GeminiProvider
from app.services.openai_service import OpenAIProvider

_registry: dict[str, AIProvider] = {}


def init_providers() -> None:
    """アプリ起動時にProviderを初期化してレジストリに登録する。"""
    _registry["openai"] = OpenAIProvider()
    _registry["gemini"] = GeminiProvider()


async def shutdown_providers() -> None:
    """アプリ終了時にProviderのリソースを解放する。"""
    for provider in _registry.values():
        await provider.close()
    _registry.clear()


def get_provider(name: str) -> AIProvider:
    """名前からProviderを取得する。"""
    if name not in _registry:
        raise ValueError(f"未対応のプロバイダ: {name} (対応: {', '.join(_registry)})")
    return _registry[name]
