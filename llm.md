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
│       ├── prompt.txt            #   Agent command (Task / Input / Output with relative paths)
│       └── <input-files>         #   Input files (PDF, PPTX, images, code, etc.)
├── iterations/                   # Development logs organized by version
│   └── <version>/
│       ├── <test-name>_self_reflection.md
│       ├── <test-name>_plan.md
│       └── <files>/              #   Supporting files (diffs, screenshots, logs)
├── results/                      # Agent output from test runs
│   └── <test-name>/              #   Mirrors test folder name
│       └── <output-files>        #   Whatever the agent produces
├── scripts/
│   └── deploy.sh                 # Copy core/ files to Cursor config directories
├── history.md                    # Version history (append-only)
├── llm.md                        # This file — workspace conventions and workflow
├── README.md                     # Public-facing project documentation
└── .gitignore
```

### What Goes to GitHub

| Tracked | Not tracked |
|---------|-------------|
| `core/`, `scripts/`, `README.md`, `history.md`, `llm.md`, `.gitignore` | `tests/`, `iterations/`, `results/` |

---

## Naming Conventions

| Item | Convention | Example |
|------|-----------|---------|
| Directories | lowercase, hyphen-separated | `cv2-homework3` |
| Agent files | lowercase, hyphen-separated `.md` | `qa-specialist.md` |
| Test folders | descriptive, hyphen-separated | `aml-assignment1` |
| Results folders | same name as test folder | `results/aml-assignment1/` |
| Version dirs under iterations/ | `v<N>` | `v1`, `v2` |
| Self-reflection files | `<test-name>_self_reflection.md` | `cv2-homework3_self_reflection.md` |
| Plan files | `<test-name>_plan.md` | `cv2-homework3_plan.md` |
| Scripts | lowercase, hyphen or underscore | `deploy.sh` |

---

## Core File Roles

| File | Deploys To | Role |
|------|-----------|------|
| `core/agent.md` | `~/.cursor/commands/agent.md` | Orchestrator: plans, delegates, manages quality. Never executes directly. |
| `core/subagents/executor.md` | `~/.cursor/agents/executor.md` | General-purpose hands-on implementation. |
| `core/subagents/designer.md` | `~/.cursor/agents/designer.md` | Visual deliverables (PDF, web, slides). Formats only, never alters content. |
| `core/subagents/debugger.md` | `~/.cursor/agents/debugger.md` | Targeted fixes within `<allowed_files>` scope. |
| `core/subagents/qa-specialist.md` | `~/.cursor/agents/qa-specialist.md` | Read-only output quality inspection (Full / Lightweight). |
| `core/subagents/verifier.md` | `~/.cursor/agents/verifier.md` | Per-item PASS/FAIL checks against explicit criteria. |
| `core/subagents/file-explorer.md` | `~/.cursor/agents/file-explorer.md` | Document extraction and organization (PDF, DOCX, PPTX). |

---

## Test Cases

Each test case is a folder under `tests/` with a `prompt.txt` and input files.

### prompt.txt Format

```
Task: <one-sentence description>
Input: <relative paths from project root, comma-separated>
Output: <relative paths under results/, comma-separated>
```

All paths are relative to the project root (`general-coding-agent/`). Input paths point to `tests/<test-name>/...`, output paths point to `results/<test-name>/...`.

### Running a Test

1. Open Cursor in the working directory where the agent should execute.
2. Copy the `Task:` line from `prompt.txt` as the agent command.
3. Attach the input files referenced in `Input:`.
4. Agent output goes to the path specified in `Output:`.

---

## Results

Agent output from test runs is saved under `results/`, mirroring the test folder name:

```
results/
└── <test-name>/              # Same name as tests/<test-name>/
    └── <output-files>        # Whatever the agent produced
```

Results are not tracked in git. They are local artifacts for evaluation.

---

## Iterations

The `iterations/` directory tracks the development process across versions.

### Structure

```
iterations/
└── v1/                                       # Version directory
    ├── cv2-homework3_self_reflection.md       # What happened, what went wrong, proposed fixes
    ├── cv2-homework3_plan.md                  # Planned changes based on reflection
    ├── aml-assignment1_self_reflection.md     # Another test case reflection
    └── files/                                 # Supporting artifacts
        ├── diff_agent_v1_v2.md                # Before/after diffs
        ├── screenshot_qa_failure.png          # Evidence
        └── execution_log.txt                  # Raw logs
```

### Self-Reflection File

Written after running a test case. Captures what the agent actually did vs. what it should have done.

Required sections:
1. **Actual Execution Flow** — Step-by-step table: action, agent used, model, notes.
2. **Issues Found** — Protocol violations and behavioral problems, each with severity, rule violated, what happened, impact.
3. **Root Cause Analysis** — Why the issues occurred (prompt gaps, ambiguous rules, missing guardrails).
4. **Proposed Fixes** — Specific, actionable changes to `core/` files. Reference exact sections/lines.

### Plan File

Written before making changes to `core/`. Translates reflection findings into an editing plan.

Required sections:
1. **Issues to Address** — Which reflection findings are being fixed (reference by ID).
2. **Changes** — Per-file list: file path, section, current text, proposed text, rationale.
3. **Test Plan** — Which test case(s) to re-run to verify the fix.

### Files Directory

Optional. Supporting artifacts that provide evidence or context:
- Diffs showing before/after of core file changes
- Screenshots of agent behavior
- Execution logs or transcripts
- Any other evidence referenced in reflections or plans

---

## Iteration Workflow

### 1. Test

Pick a test case from `tests/`. Use the prompt in `prompt.txt` as the agent command. Run in a real Cursor session.

### 2. Observe

Examine the agent's behavior:
- Did it delegate correctly or do things itself?
- Were subagent dispatches well-scoped with full context?
- Did the QA loop catch real issues?
- Were independent tasks dispatched in parallel?
- Where did it fail or produce low-quality output?

### 3. Reflect

Write `iterations/<version>/<test-name>_self_reflection.md` following the required sections above. Be specific — quote the rules that were violated, show the actual behavior, analyze root cause.

### 4. Plan

Write `iterations/<version>/<test-name>_plan.md` translating findings into concrete edits. Every change must reference a specific issue from the reflection.

### 5. Update

Edit files in `core/` based on the plan:
- **Surgical edits only.** Change exactly what needs to change.
- **One concern per change.** Don't bundle unrelated fixes.
- **Preserve structure.** Keep existing section names, XML tags, and formatting.
- **Keep descriptions in sync.** If you change a subagent's behavior, update its description row in the `<team>` table in `agent.md`.

### 6. Deploy

```bash
./scripts/deploy.sh
```

### 7. Verify

Re-run the same test case (or a relevant one) to confirm the fix works and didn't break other behavior.

### 8. Version

After a batch of changes stabilizes:
- Update `history.md` with a new version entry (append — never modify past entries).
- Commit to GitHub with a descriptive message.

---

## Update Rules

### Core File Editing

- **Never rename XML tags** in `agent.md` (e.g., `<role>`, `<team>`, `<rules>`, `<workflow>`) without verifying no external references depend on them.
- **Never remove a subagent file** without removing its row from the `<team>` table and model defaults table in `agent.md`.
- **Adding a new subagent**: create `core/subagents/<name>.md`, add a row to the `<team>` table, add a model default row. `deploy.sh` auto-discovers `*.md` files — no script change needed.
- **Changing subagent scope/behavior**: update both the subagent's `.md` file AND its description in the `<team>` table. These must stay in sync.

### Version Management

- `history.md` is **append-only**. Never modify past version entries. Only add new versions at the top.
- Each version entry should list: architecture changes, new/modified subagents, workflow changes, QC changes, and which test cases validated the changes.

### Deployment

- Always run `./scripts/deploy.sh` after editing `core/` files.
- The script copies `core/agent.md` to `~/.cursor/commands/agent.md` and `core/subagents/*.md` to `~/.cursor/agents/`.
- Verify the deployment by checking file timestamps or diffing.
