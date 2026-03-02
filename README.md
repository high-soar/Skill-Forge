# Skill-Forge

## 言語

日本語で対応すること

## 概要

実行と振り返りのサイクルを通じて、エージェント能力の精度と信頼性を極めるためのスキルセット

現在、以下のスキル群を管理・プロセスに組み込んでいます。

### 🤖 スキル一覧

*   **[skill-manager](./skills/skill-manager/)**
    エージェントスキルのライフサイクル（作成、レビュー、改善）を総合的に管理します。新規スキルの作成や、問題が発生した際の改善ワークフローを実行します。

*   **[review-process](./skills/review-process/)**
    設計書やソースコード等の開発成果物に対し、「悪魔の代弁者（Devil's Advocate）」の視点で徹底的なレビューとその修正対応・検証・水平展開のライフサイクルを回すためのスキルです。

*   **[conducting-retrospective](./skills/conducting-retrospective/)**
    対話の履歴を分析し、ユーザーから受けた指摘事項の特定、根本原因の分析（スキル不備、コンテキスト不足など）、および改善策やスキルへのフィードバックを検討する「振り返り（レトロスペクティブ）」を実施するスキルです。

## ディレクトリ構成

skills配下に開発対象のスキルを作成していく。

```text
.
└── skills/
    ├── skill-manager/
    ├── review-process/
    └── conducting-retrospective/
```
