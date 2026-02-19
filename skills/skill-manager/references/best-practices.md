# Skill Design Best Practices

> Distilled from the "Agent Skills Creation & Improvement Guide"

## 1. Description Engineering

The `description` field in the frontmatter determines the skill discovery accuracy.

### name Field
- **Max 64 characters**, kebab-case (`lowercase-with-hyphens`).
- "Verb-gerund + noun" pattern recommended (e.g., `processing-pdfs`, `testing-code`).
- **Avoid**: Ambiguous names like `utils`, `helper`, or reserved words like `anthropic`, `claude`.

### description Field
- **Max 1024 characters**, written in the third person (avoid first person).
- Should include:
  - A summary of the function the skill performs.
  - **Specific keywords/file extensions** the user is likely to use.
  - **Negative Triggers**: Exclusion conditions to prevent false positives.

**Good Example:**
```
Analyzes Excel spreadsheets, creates pivot tables, and generates charts.
Use when the user requests analysis of Excel files, tabular data, or .xlsx files.
Do NOT use for reading simple CSV files.
```

**Bad Example:**
```
Helps with processing documents.
```

## 2. Context Window Management

### SKILL.md Body Limits
- Strictly keep within **500 lines**.
- Omit redundant explanations of general knowledge known to LLMs.
- Focus only on tacit knowledge or unique rules specific to the target domain.

### Avoid Nested References
- Formatting references from SKILL.md to external files should be **1 level deep only**.
- Deep nesting like File A → B → C is prohibited.
- all references must be linked flatly and directly from SKILL.md.

### Progressive Disclosure
| Level | Content | Loading Timing |
|:--|:--|:--|
| L1: Metadata | name + description (~100 words) | Always |
| L2: Instructions | SKILL.md body (<5000 words) | Upon skill trigger |
| L3: Resources | scripts/, references/, assets/ | Only when needed |

## 3. Controlling Degrees of Freedom

Adjust the specificity of instructions according to the nature of the task.

| Degree | Application | Instruction Format |
|:--|:--|:--|
| **High** | Code review, brainstorming | Natural language heuristics |
| **Medium** | Report generation, API spec creation | Output templates |
| **Low** | DB migration, data parsing | Mandatory validation scripts |

## 4. Addressing Model Laziness

Countermeasures for the Agent's tendency to skip steps:
- Introduce **checklist-style** workflows.
- Include explicit encouragement phrases:
  - "Take your time to do this thoroughly"
  - "Quality is more important than speed"
  - "Do not skip validation steps"

## 5. Troubleshooting

| Symptom | Root Cause | Remedy |
|:--|:--|:--|
| Skill not triggered | `description` is vague or diverges from user vocabulary | Make trigger phrases more specific |
| Over-triggered on unrelated tasks | `description` scope is too broad | Add negative triggers |
| Unstable output format | Degree of freedom is too high | Strict templates |
| Steps are skipped | Model laziness | Checklists + Encouragement phrases |

## 6. Shared Information Architecture

Approaches for sharing common formats across multiple skills:

| Approach | Application | Pros | Cons |
|:--|:--|:--|:--|
| **A: Via MCP** | Enterprise | Real-time sync, centralized management | Infrastructure cost |
| **B: Relative Path to Shared File** | Local Dev | Fast, Git-managed | Restricted to repository |
| **C: Reference Skill** | Large Shared Knowledge | Encapsulation | Reliability of chained calls |
| **D: CLAUDE.md Global Rules** | Small/Universal Rules | Easy implementation | Constant token consumption |

