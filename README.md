# AI API Token Usage POC

ChatGPT (OpenAI) と Gemini (Google) の API を実行し、トークン使用量 (input / output / total) を確認・記録するための POC 環境。

## 構成

- **FastAPI** - REST API サーバー
- **Docker** - 実行環境
- **CSV** - トークン使用量のログ保存

## セットアップ

```bash
# 環境変数ファイルを作成し、APIキーを記入
cp .env.example .env

# 起動
docker compose up --build
```

起動後、http://localhost:8000/docs で Swagger UI を確認できます。

## API エンドポイント

| Method | Endpoint | 説明 |
|--------|----------|------|
| POST | `/api/v1/chat/openai` | OpenAI API を実行 |
| POST | `/api/v1/chat/gemini` | Gemini API を実行 |
| GET | `/api/v1/usage/logs` | トークン使用量ログを取得 |
| GET | `/health` | ヘルスチェック |

### リクエスト例

```bash
curl -X POST http://localhost:8000/api/v1/chat/gemini \
  -H "Content-Type: application/json" \
  -d '{"prompt_key": "greeting"}'
```

### レスポンス例

```json
{
  "response": "こんにちは。私は...",
  "usage": {
    "input_tokens": 25,
    "output_tokens": 120,
    "total_tokens": 145
  },
  "model": "gemini-3.1-pro-preview",
  "provider": "gemini"
}
```

## 環境変数

| 変数 | 説明 | デフォルト |
|------|------|-----------|
| `OPENAI_API_KEY` | OpenAI API キー | - |
| `OPENAI_MODEL` | 使用モデル | `o3` |
| `OPENAI_REASONING_EFFORT` | 推論レベル (low/medium/high) | `high` |
| `GEMINI_API_KEY` | Gemini API キー | - |
| `GEMINI_MODEL` | 使用モデル | `gemini-3.1-pro-preview` |
| `GEMINI_THINKING_LEVEL` | 3.x系の思考レベル (minimal/low/medium/high) | `high` |
| `GEMINI_THINKING_BUDGET` | 2.5系の思考バジェット (-1で動的) | `-1` |
| `GEMINI_TEMPERATURE` | Temperature | `0.0` |

## プロンプト管理

`config/prompts.yaml` にプロンプトを定義し、`prompt_key` で指定して実行します。

```yaml
prompts:
  cost_estimation:
    system: "あなたはフィットネスサロンのアドバイザーです。"
    user: "以下のデータを基にアドバイスしてください: {data}"
```

変数は `variables` パラメータで置換できます。

```bash
curl -X POST http://localhost:8000/api/v1/chat/openai \
  -H "Content-Type: application/json" \
  -d '{"prompt_key": "cost_estimation", "variables": {"data": "体重70kg, 身長175cm"}}'
```

## ディレクトリ構成

```
.
├── .docker/Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── config/
│   └── prompts.yaml
├── app/
│   ├── main.py
│   ├── config.py
│   ├── routers/
│   │   ├── chat.py
│   │   └── usage.py
│   ├── schemas/
│   │   └── chat.py
│   └── services/
│       ├── openai_service.py
│       ├── gemini_service.py
│       ├── prompt_loader.py
│       └── token_logger.py
└── logs/
    └── token_usage.csv (自動生成)
```
