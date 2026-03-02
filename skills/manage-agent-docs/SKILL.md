---
description: A skill to maintain and generate Agent-Friendly documentation structures.
---

# `manage-agent-docs` Skill

This skill assists in maintaining a "traceable structure easily comprehensible for agents (LLMs)" for markdown documents within a project.
Documents MUST have `id` and `implements` (reference to parent document) defined via YAML Frontmatter.

## トリガー条件 (Trigger Conditions)
The skill is triggered when the user requests actions such as:
- "Check document consistency" / "Lint docs" (Lint Mode)
- "Create a template for new requirement docs" (Scaffold Mode)
- "I want to write agent-friendly documentation"

## 動作モード (Operation Modes)

### 1. Lint モード (Traceability Check)
When requested to check documents, execute the following steps:

1. **チェックスクリプトの実行 (Execute Check Script)**:
   Run the following command to check the consistency of the current documents.
   ```bash
   python3 <SKILL_DIR>/scripts/traceability_checker.py <Target_Docs_Directory>
   ```
2. **結果の分析と修正提案 (Analyze Results & Propose Fixes)**:
   - If errors like duplicated/missing `id`s or broken `implements` links are output, report the error locations to the user.
   - Upon receiving permission from the user, modify the Frontmatter of the relevant Markdown files to restore traceability.

### 2. Scaffold モード (Document Generation)
When requested to create new features or design documents, execute the following steps:

1. **階層の特定 (Identify Layer)**:
   Confirm with the user which of the following layers the document belongs to:
   - **Requirement:** `type: requirement` / Template: `templates/requirement.md`
   - **Interface:** `type: interface` / Template: `templates/interface.md`
   - **Internal Design:** `type: internal_design` / Template: `templates/internal_design.md`

2. **依存関係の確認 (Confirm Dependencies)**:
   - When creating an Interface layer, ask for or search for the parent "Requirement ID".
   - When creating an Internal Design layer, ask for the parent "Requirement ID" or "Interface ID".

3. **テンプレートからの生成 (Generate from Template)**:
   Copy (or read and generate from) the corresponding template in `<SKILL_DIR>/templates/` to the target directory. Fill in the "ID", "Title", and "Implements (Parent ID)" appropriately and present it to the user.
   - After generation, if possible, run the script for Lint mode again to verify that the links are correctly established.

## ベストプラクティス (Agent-Friendly Rules)
- Natural language descriptions like "Refer to XX file" are hard for Agents to interpret. Always specify the ID in the `implements` field of the Frontmatter.
- Keep each document (file) within a size (chunk) that handles a single responsibility.
