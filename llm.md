# Agent Development Workspace Guide

This document defines the structure, conventions, and workflow for developing and iterating on the General Coding Agent system. Read this before making any changes.

---

## Workspace Structure

```
general-coding-agent/
├── core/                     # Agent definitions (source of truth)
│   ├── agent.md              #   Orchestrator (Cursor command)
│   └── subagents/            #   Subagent definitions (Cursor agents)
│       ├── debugger.md
│       ├── designer.md
│       ├── executor.md
│       ├── file-explorer.md
│       ├── qa-specialist.md
│       └── verifier.md
├── tests/                    # Test cases (not tracked in git)
│   └── <test-name>/          #   One folder per test case
│       ├── prompt.txt        #     Agent prompt (Task / Input / Output)
│       └── <input-files>     #     Input files (PDF, PPTX, images, code, etc.)
├── iterations/               # Self-reflection logs per version (not tracked in git)
│   └── <version>_<date>/
│       └── <test-name>_self_reflection.md
├── results/                  # Agent output from test runs (not tracked in git)
├── scripts/
│   └── deploy.sh             # Copy core/ files to Cursor config dirs
├── history.md                # Version history with features per release
├── llm.md                    # This file — workspace guide
├── README.md                 # Public-facing project documentation
└── .gitignore
```

## What Goes to GitHub (core code only)

Tracked: `core/`, `scripts/`, `README.md`, `history.md`, `llm.md`, `.gitignore`
Not tracked: `tests/`, `iterations/`, `results/`

---

## Naming Conventions

| Item | Convention | Example |
|------|-----------|---------|
| Directories | lowercase, hyphen-separated | `cv2-homework3`, `file-explorer` |
| Agent files | lowercase, hyphen-separated `.md` | `qa-specialist.md` |
| Test folders | descriptive, hyphen-separated | `aml-assignment1` |
| Iteration dirs | `<version>_<MMDD>` | `v1_0305` |
| Reflection files | `<test-name>_self_reflection.md` | `CV2_HM3_self_reflection.md` |
| Scripts | lowercase, hyphen or underscore | `deploy.sh` |

---

## Core File Roles

| File | Deploys To | Role |
|------|-----------|------|
| `core/agent.md` | `~/.cursor/commands/agent.md` | Orchestrator: plans, delegates, manages quality. Never executes directly. |
| `core/subagents/executor.md` | `~/.cursor/agents/executor.md` | General-purpose hands-on implementation. |
| `core/subagents/designer.md` | `~/.cursor/agents/designer.md` | Visual deliverables (PDF, web, slides). Content-agnostic — formats only. |
| `core/subagents/debugger.md` | `~/.cursor/agents/debugger.md` | Targeted fixes within scoped file list. |
| `core/subagents/qa-specialist.md` | `~/.cursor/agents/qa-specialist.md` | Read-only output quality inspection (Full / Lightweight). |
| `core/subagents/verifier.md` | `~/.cursor/agents/verifier.md` | Per-item PASS/FAIL checks against explicit criteria. |
| `core/subagents/file-explorer.md` | `~/.cursor/agents/file-explorer.md` | Document extraction and organization (PDF, DOCX, PPTX). |

---

## Iteration Workflow

### 1. Test

Pick a test case from `tests/`. Use the prompt in `prompt.txt` as the agent command. Run the agent against it in a real Cursor session.

### 2. Observe

Examine the agent's behavior: delegation patterns, quality of subagent output, QA loop effectiveness, parallelism, failure modes.

### 3. Reflect

Write `iterations/<version>_<MMDD>/<test-name>_self_reflection.md` with:
- Actual execution flow (step-by-step table)
- Protocol violations (what the agent did wrong vs. its own rules)
- Root cause analysis
- Proposed fixes (specific, actionable changes to core files)

### 4. Update

Edit files in `core/` based on reflection findings. Follow these rules:
- **Surgical edits only.** Change exactly what needs to change. Don't refactor unrelated sections.
- **One concern per change.** Don't bundle unrelated fixes.
- **Preserve structure.** Keep existing section names, XML tags, and formatting conventions.
- **Test the change.** Re-run the same test case (or a relevant one) to verify the fix works.

### 5. Deploy

```bash
./scripts/deploy.sh
```

### 6. Version

After a batch of changes stabilizes:
- Update `history.md` with a new version entry listing features and changes.
- Commit to GitHub with a descriptive message.

---

## Update Rules

- **Never rename XML tags** in agent.md (e.g., `<role>`, `<team>`, `<rules>`, `<workflow>`) without updating all references.
- **Never remove a subagent** without removing it from the `<team>` table in `agent.md`.
- **Adding a new subagent**: create `core/subagents/<name>.md`, add a row to the `<team>` table, add a model default row, and update `deploy.sh` if needed (current script auto-discovers `*.md`).
- **Changing subagent scope/behavior**: update both the subagent file AND its description in the `<team>` table (they must stay in sync).
- **history.md** is append-only. Never modify past version entries.

---

## Test Case Format

Each test case lives in `tests/<test-name>/` and contains:

```
tests/<test-name>/
├── prompt.txt        # Agent command: Task, Input, Output (keep it minimal)
└── <input-files>     # Whatever the agent needs to work with
```

`prompt.txt` format:
```
Task: <one-sentence description of what to do>
Input: <list of input files with brief description>
Output: <expected deliverables>
```
