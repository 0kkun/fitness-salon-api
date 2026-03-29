---
paths:
  - "app/**/*.py"
---

# アーキテクチャ

```
app/
├── main.py           # FastAPIアプリ定義、lifespan、例外ハンドラ
├── config.py         # pydantic-settingsによる設定管理
├── providers.py      # AIProviderレジストリ (初期化・取得・解放)
├── schemas/          # Pydanticモデル (リクエスト/レスポンス)
├── routers/          # APIエンドポイント
└── services/         # ビジネスロジック
    ├── base.py       # AIProvider ABC (共通インターフェース)
    ├── openai_service.py
    ├── gemini_service.py
    ├── prompt_loader.py
    └── token_logger.py
config/prompts.yaml   # プロンプトテンプレート定義
tests/                # pytest テスト
```

## API

統合エンドポイント: `POST /api/v1/chat`

```json
{"provider": "openai", "prompt_key": "greeting", "variables": {"data": "..."}}
```

## Provider追加手順

1. `app/services/` に `AIProvider` を継承したクラスを作成
2. `app/providers.py` の `init_providers()` にレジストリ登録を追加
