---
paths:
  - "**/*.py"
---

# コーディング規約

- 非同期 (async/await) を基本とする
- AI APIコールには `@ai_retry` デコレータを適用する
- トークンログはCSV形式 (`logs/token_usage.csv`) で記録する
