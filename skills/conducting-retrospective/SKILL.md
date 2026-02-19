---
name: conducting-retrospective
description: Conducts structured retrospectives by analyzing conversation thread history, identifying issues pointed out by the user, performing root cause analysis, and discussing improvements. Use when the user requests '振り返り', 'retrospective', '反省', '改善', 'ふりかえり', 'retro', or 'review my feedback'. Covers analysis of skill defects, custom instruction issues, context gaps, and judgment errors. Do NOT use for general code review, skill creation, or skill quality checks — use skill-manager for those.
---

# Conducting Retrospective

Analyze conversation history to identify user-reported issues, determine root causes, and drive continuous improvement of Agent skills and custom instructions.

## Workflow Overview

A retrospective involves three sequential steps. Take your time to do this thoroughly.

1. Analyze thread history → Extract user-reported issues
2. Perform root cause analysis → Discuss findings with user
3. Execute improvements → Modify skills or custom instructions

---

## Step 1: Thread Analysis

Scan the current conversation thread and extract every instance where the user:

- Corrected the Agent's output or behavior
- Pointed out errors, omissions, or misunderstandings
- Expressed dissatisfaction or requested changes
- Had to repeat or clarify instructions

For each identified issue, record:

| Field | Description |
|:--|:--|
| **事象** | What happened — the observable incorrect behavior |
| **ユーザの指摘** | What the user said or did to correct it |
| **発生箇所** | Where in the thread (approximate position or quote) |

Present the extracted list to the user and confirm completeness before proceeding to Step 2.

## Step 2: Root Cause Analysis & Discussion

For each confirmed issue, analyze the root cause using this classification:

| Cause Category | Description | Examples |
|:--|:--|:--|
| **スキル不備** | Skill instructions are missing, ambiguous, or incorrect | Missing step, vague instruction, wrong template |
| **カスタム指示不備** | Global rules or project rules caused or failed to prevent the issue | MEMORY rules conflicting, missing rule |
| **コンテキスト不足** | Agent lacked necessary context to make the right decision | File not read, requirements unclear |
| **判断ミス** | Agent had sufficient information but made wrong judgment | Ignored instruction, chose wrong approach |

For each issue, also assign a severity:

| Severity | Criteria |
|:--|:--|
| **Critical** | Same error has occurred repeatedly, or high impact on deliverables |
| **Major** | Significant quality degradation or wasted user effort |
| **Minor** | Cosmetic or low-impact issue, easily corrected |

### Analysis Output Per Issue

For each issue, produce the following structured analysis:

```
### 指摘 N: [短いタイトル]

- **事象**: [何が起きたか]
- **重要度**: Critical / Major / Minor
- **原因分類**: スキル不備 / カスタム指示不備 / コンテキスト不足 / 判断ミス
- **原因詳細**: [なぜ起きたかの具体的分析。特にスキルやカスタム指示に起因する場合はどの指示が関連するか特定]
- **改善策**: [具体的な対応提案]
```

Present the full analysis to the user and discuss:
- Whether the cause classification is correct
- Whether the proposed improvements are appropriate
- Whether there are additional patterns or systemic issues

Quality is more important than speed. Ensure the user agrees with the analysis before proceeding.

## Step 3: Execute Improvements

Based on the agreed analysis, determine the improvement actions:

### Skill Modifications

If skills require modification:

1. Identify the target skill and specific section to change
2. Check if a skill modification skill exists (e.g., skill-manager Improvement Workflow)
3. **If a modification skill exists, delegate to it** — read and follow its instructions
4. If no modification skill exists, apply changes directly and run validation

### Custom Instruction Modifications

If custom instructions (MEMORY, project rules, etc.) require modification:

1. Present the current instruction and proposed change to the user
2. **Wait for explicit user approval** before making any changes
3. Apply the approved modifications
4. Confirm the changes with the user

### No Action Required

If the root cause is コンテキスト不足 or 判断ミス with no systemic fix, document the finding in the retrospective report for future awareness.

---

## Retrospective Report

After completing all three steps, generate a retrospective report using the template in [retrospective-template.md](references/retrospective-template.md).

Output the report content directly in the conversation.

Then, save the report to a file:
1. Default location: `docs/retrospectives/YYYY-MM-DD-retrospective.md` (append counter if multiple in same day)
2. If the user specifies a different location, use that instead.
3. Automatically create the directory if it doesn't exist.

---

## Trend Analysis

When multiple retrospectives have been conducted, look for recurring patterns:

- Issues with the same cause category appearing repeatedly
- The same skill being flagged across multiple retrospectives
- Severity trends (improving or worsening)

Document trends in the report to support long-term improvement.
