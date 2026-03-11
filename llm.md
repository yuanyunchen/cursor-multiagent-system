# Agent Development Workspace Guide

Read this document before making any changes to the General Coding Agent system.

---

## Workspace Structure

```
general-coding-agent/
├── core/                         # Source of truth — agent definitions
│   ├── agent.md                  #   Orchestrator (deploys to ~/.cursor/commands/)
│   └── subagents/                #   Subagent definitions (deploy to ~/.cursor/agents/)
│       ├── debugger.md
│       ├── designer.md
│       ├── executor.md
│       ├── file-explorer.md
│       ├── qa-specialist.md
│       └── verifier.md
├── tests/                        # Test cases for evaluating agent behavior
│   └── <test-name>/
│       ├── prompt.txt            #   Agent command (Task / Input / Output)
│       └── <input-files>         #   PDF, PPTX, images, code, etc.
├── iterations/                   # Development logs organized by version
│   └── <version>/
│       ├── <test-name>_self_reflection.md
│       ├── <test-name>_plan.md
│       └── files/                #   Diffs, screenshots, logs
├── results/                      # Agent output from test runs
│   └── <version>_<date>/
│       └── <output-files>
├── current -> iterations/<version>  # Symlink to current version's iteration files
├── scripts/
│   └── deploy.sh                 # Copy core/ to Cursor config directories
├── history.md                    # Version history (append-only)
├── llm.md                        # This file
├── README.md                     # Public-facing documentation
└── .gitignore
```

### What Goes to GitHub

| Tracked | Not tracked |
|---------|-------------|
| `core/`, `scripts/`, `README.md`, `history.md`, `llm.md`, `.gitignore` | `tests/`, `iterations/`, `results/` |

---

## Naming Conventions

| Item | Rule | Example |
|------|------|---------|
| Directories | lowercase, hyphen-separated | `cv2-homework3` |
| Agent files | lowercase, hyphen-separated `.md` | `qa-specialist.md` |
| Test folders | descriptive, hyphen-separated | `aml-assignment1` |
| Results folders | `<version>_<MMDD>` | `results/v1_0310/` |
| Iteration version dirs | `v<N>` | `iterations/v1/` |
| Self-reflection files | `<test-name>_self_reflection.md` | `cv2-homework3_self_reflection.md` |
| Plan files | `<test-name>_plan.md` | `cv2-homework3_plan.md` |

### prompt.txt Format

```
Task: <one-sentence description>
Input: tests/<test-name>/<file>, tests/<test-name>/<file>
Output: results/<version>_<date>/<output-files>
```

All paths relative to project root. Version and date in Output are provided at test time.

---

## Core File Roles

| File | Deploys To | Role |
|------|-----------|------|
| `core/agent.md` | `~/.cursor/commands/agent.md` | Orchestrator: plans, delegates, manages quality. |
| `core/subagents/executor.md` | `~/.cursor/agents/executor.md` | General-purpose implementation. |
| `core/subagents/designer.md` | `~/.cursor/agents/designer.md` | Visual deliverables (PDF, web, slides). |
| `core/subagents/debugger.md` | `~/.cursor/agents/debugger.md` | Targeted fixes within scoped file list. |
| `core/subagents/qa-specialist.md` | `~/.cursor/agents/qa-specialist.md` | Read-only output quality inspection. |
| `core/subagents/verifier.md` | `~/.cursor/agents/verifier.md` | Per-item PASS/FAIL checks. |
| `core/subagents/file-explorer.md` | `~/.cursor/agents/file-explorer.md` | Document extraction and organization. |

---

## Iterations

```
iterations/
└── v1/
    ├── cv2-homework3_self_reflection.md    # Execution flow, issues, root cause, proposed fixes
    ├── cv2-homework3_plan.md               # Concrete edit plan based on reflection
    └── files/                              # Supporting artifacts (diffs, screenshots, logs)
```

**Self-reflection** — what the agent actually did vs. what it should have done:
1. Actual execution flow (step-by-step table)
2. Issues found (severity, rule violated, what happened, impact)
3. Root cause analysis
4. Proposed fixes (reference specific sections in `core/` files)

**Plan** — translates reflection into edits:
1. Issues to address (reference reflection IDs)
2. Per-file changes (file, section, current text, proposed text, rationale)
3. Test plan (which test case to re-run)

---

## Version Update Checklist

When releasing a new version after changes stabilize:

### 1. Core files (`core/`)

- [ ] Edit `core/agent.md` and/or `core/subagents/*.md` as needed
- [ ] If a subagent's behavior changed: update BOTH the subagent `.md` file AND its row in the `<team>` table in `agent.md` (must stay in sync)
- [ ] If a subagent's model default changed: update the model defaults table in `agent.md`
- [ ] If adding a new subagent: create `core/subagents/<name>.md` + add `<team>` row + add model default row (`deploy.sh` auto-discovers `*.md`)
- [ ] If removing a subagent: delete the file + remove its `<team>` row + remove its model default row
- [ ] Never rename XML tags in `agent.md` (`<role>`, `<team>`, `<rules>`, `<workflow>`) without checking all references

### 2. Update `current` symlink

```bash
rm current && ln -s iterations/<version> current
```

### 3. Deploy

```bash
./scripts/deploy.sh
```

Copies `core/agent.md` -> `~/.cursor/commands/agent.md`, `core/subagents/*.md` -> `~/.cursor/agents/`.

### 4. Test

Re-run relevant test cases to verify changes work and nothing regressed.

### 5. Document

- [ ] `iterations/<version>/` — add self-reflection and plan files for this version
- [ ] `history.md` — append a new version entry (never modify past entries). Include: what changed, why, which subagents were modified, which test cases validated it.

### 6. Commit

```bash
git add -A && git commit -m "<message>" && git push
```

Commit message format: `v<N>: <short summary>` with bullet points for specific changes.
