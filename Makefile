# ---------- 共通変数 ----------
API_CONTAINER=api


# ---------- Commands ----------
.PHONY: help up down build restart logs app


# =============================
# Help
# =============================
help: ## コマンド一覧を表示
	@echo ""
	@echo "📘 Make Commands"
	@echo "----------------------------------------"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo ""


# =============================
# コンテナ管理
# =============================
build: ## イメージをビルドして起動
	docker compose up -d --build
up: ## コンテナを起動
	docker compose up -d
down: ## コンテナを停止・削除
	docker compose down --remove-orphans
restart: ## コンテナを再起動
	docker compose down --remove-orphans
	docker compose up -d
logs: ## コンテナのログを表示
	docker compose logs -f $(API_CONTAINER)
app: ## APIコンテナにシェルで入る
	docker compose exec $(API_CONTAINER) sh
test: ## テストを実行
	docker compose exec $(API_CONTAINER) pytest tests/ -v


# =============================
# コード品質
# =============================
lint: ## Ruffでlintチェック
	docker compose exec $(API_CONTAINER) ruff check .
format: ## Ruffでフォーマット
	docker compose exec $(API_CONTAINER) ruff format .
lint-fix: ## Ruffでlint自動修正
	docker compose exec $(API_CONTAINER) ruff check --fix .
