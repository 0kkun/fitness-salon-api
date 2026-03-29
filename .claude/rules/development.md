# 開発環境

- Python 3.12 (Docker上で動作)
- フレームワーク: FastAPI + Uvicorn
- パッケージ管理: requirements.txt (pip)

## コマンド

すべてDocker経由で実行する。ローカルのPythonは使わない。

```bash
make build    # イメージをビルドして起動
make up       # コンテナを起動
make down     # コンテナを停止・削除
make restart  # コンテナを再起動
make logs     # ログを表示
make app      # コンテナにシェルで入る
make test     # テストを実行
```
