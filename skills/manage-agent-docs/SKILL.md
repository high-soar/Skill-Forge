---
name: manage-agent-docs
description: 'Maintains and generates Agent-Friendly documentation structures with YAML Frontmatter traceability. Use when the user requests any of: "lint docs", "check traceability", "check document consistency", "create requirement doc", "create design doc", "scaffold docs", "agent-friendly documentation", "ドキュメント整合性チェック", "要件書作成", "設計書作成". Do NOT use for general markdown editing, code review, README generation, or API documentation.'
---

# `manage-agent-docs` Skill

Maintain a traceable, Agent-readable documentation structure for Markdown files in a project.
All managed documents MUST define `id` and `implements` (reference to parent document) in YAML Frontmatter.

## Operation Modes

### 1. Lint Mode (Traceability Check)

When asked to check or lint documents:

1. **Execute the check script**:
   ```bash
   python3 <SKILL_DIR>/scripts/traceability_checker.py <Target_Docs_Directory>
   ```
2. **Report results**:
   - If errors (duplicate/missing `id` or broken `implements` links) are found, show each error location to the user.
   - With user permission, fix the Frontmatter of affected files to restore traceability.

### 2. Scaffold Mode (Document Generation)

When asked to create a new document:

1. **Identify the target directory**:
   - Search the project for an existing docs directory (e.g., `docs/`, `requirements/`, `design/`).
   - If ambiguous, ask the user: "Which directory should I place this document in?"

2. **Identify the document layer**:
   Confirm with the user which layer the document belongs to:
   - **Requirement:** `type: requirement` / Template: `templates/requirement.md`
   - **Interface:** `type: interface` / Template: `templates/interface.md`
   - **Internal Design:** `type: internal_design` / Template: `templates/internal_design.md`

3. **Confirm dependencies**:
   - Interface layer: ask for or search for the parent Requirement ID.
   - Internal Design layer: ask for the parent Requirement ID or Interface ID.

4. **Generate from template**:
   - Copy the corresponding file from `<SKILL_DIR>/templates/` to the target directory.
   - Do **not** load the template into context—copy it as a file, then open and fill in `id`, `title`, and `implements` only.
   - After generation, run the Lint Mode script to confirm the links are correctly established.

## Agent-Friendly Rules

- Always use the `implements` Frontmatter field to reference parent documents by ID—never by filename or natural-language phrases like "Refer to XX file".
- Keep each document within a single-responsibility scope (one concern per file).
