# AI API トークン使用量確認環境（POC）

## 概要
- ChatGPT（OpenAI）およびGemini（Google）のAPIを実行し、input / output / total のトークン使用量を確認できるローカルPOC環境を構築する
- コスト試算のための事前検証として、各APIのトークン消費量を定量的に把握することが目的

## スコープ
- **含む**
  - OpenAI Chat Completions API の実行・トークン使用量取得
  - Google Gemini API の実行・トークン使用量取得
  - トークン使用量（input_tokens, output_tokens, total_tokens）のCSVログ保存
  - FastAPI による REST API サーバー構築
  - Docker を使用した実行環境
- **含まない**
  - 本番環境へのデプロイ
  - 認証・認可の仕組み
  - フロントエンドUI
  - プロンプトの最適化・改善（別タスクで実施）

## 機能要件
- [ ] OpenAI API を呼び出し、レスポンスとトークン使用量を取得できる
- [ ] Gemini API を呼び出し、レスポンスとトークン使用量を取得できる
- [ ] 各API呼び出しの結果として以下を返却する
  - AIのレスポンステキスト
  - input_tokens（入力トークン数）
  - output_tokens（出力トークン数）
  - total_tokens（合計トークン数）
  - 使用したモデル名
- [ ] トークン使用量をCSVファイルに自動記録する
- [ ] 設定ファイルからプロンプトを読み込んで実行できる

## 非機能要件
- **セキュリティ**: APIキーは環境変数で管理し、ソースコードにハードコードしない
- **可用性**: ローカルPOC環境のため、可用性要件なし

## API仕様

### エンドポイント一覧

#### `POST /api/v1/chat/openai`
- OpenAI API を実行しトークン使用量を返却する
- リクエスト:
  ```json
  {
    "prompt_key": "string (設定ファイル内のプロンプトキー)",
    "model": "string (任意。デフォルト: gpt-4o)",
    "variables": { "key": "value (プロンプト内の変数置換用、任意)" }
  }
  ```
- レスポンス:
  ```json
  {
    "response": "string",
    "usage": {
      "input_tokens": 0,
      "output_tokens": 0,
      "total_tokens": 0
    },
    "model": "string",
    "provider": "openai"
  }
  ```

#### `POST /api/v1/chat/gemini`
- Gemini API を実行しトークン使用量を返却する
- リクエスト/レスポンス構造は OpenAI と同一（`provider` が `"gemini"` になる）

#### `GET /api/v1/usage/logs`
- CSVに記録されたトークン使用量ログを取得する
- レスポンス:
  ```json
  {
    "logs": [
      {
        "timestamp": "ISO8601",
        "provider": "openai|gemini",
        "model": "string",
        "prompt_key": "string",
        "input_tokens": 0,
        "output_tokens": 0,
        "total_tokens": 0
      }
    ]
  }
  ```

## CSVログ仕様
- 保存先: `logs/token_usage.csv`
- カラム: `timestamp, provider, model, prompt_key, input_tokens, output_tokens, total_tokens`

## プロンプト設定ファイル
- 形式: YAML
- 保存先: `config/prompts.yaml`
- 構造例:
  ```yaml
  prompts:
    cost_estimation:
      system: "あなたはフィットネスサロンのアドバイザーです。"
      user: "以下のデータを基にアドバイスしてください: {data}"
  ```

## 依存関係
- OpenAI Python SDK (`openai`)
- Google Generative AI SDK (`google-generativeai`)
- FastAPI + Uvicorn
- Docker / Docker Compose（既存の `.docker` 構成を活用）

## 制約・前提条件
- OpenAI および Google の APIキーを事前に取得済みであること
- ローカル開発環境（Docker Desktop）が利用可能であること
- プロンプトの叩き台と参照データは別途共有される予定

## 未決事項
- [ ] 使用するモデルの具体的なバージョン（gpt-4o / gemini-1.5-pro 等）
- [ ] プロンプトの具体的な内容（叩き台の共有待ち）
- [ ] 参照データの形式・サイズ
- [ ] 既存の `.docker` 構成との統合方針
