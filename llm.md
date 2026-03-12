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
│       ├── requirements/          #   Feature requirements for this version
│       │   └── <feature-name>.md
│       ├── problems.md            #   Consolidated issue list
│       ├── code_review.md         #   Code review findings
│       ├── human_feedback.md      #   User feedback from test runs
│       ├── <test-name>_self_reflection.md
│       ├── <test-name>_plan.md
│       └── files/                #   Archived core/ snapshot, diffs, screenshots, logs
│           └── core/             #   Snapshot of core/ at this version
├── results/                      # Agent output from test runs
│   └── <version>/
│       └── <test-name>/
│           └── <output-files>
├── current -> iterations/<version>  # Symlink to current version's iteration files
├── scripts/
│   └── deploy.sh                 # Sync core/ to Cursor; --archive saves to current iteration
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
| Results folders | `<version>/<test-name>/` | `general-coding-agent/results/v1.2/aml-assignment1/` |
| Session name | `<version>_<test-name>_<model>` | `v1.2_aml-assignment1_gpt-5.4` |
| Iteration version dirs | `v<N>` | `iterations/v1/` |
| Self-reflection files | `<test-name>_self_reflection.md` | `cv2-homework3_self_reflection.md` |
| Plan files | `<test-name>_plan.md` | `cv2-homework3_plan.md` |

### prompt.txt Format

```
Task: <one-sentence description>
Input: general-coding-agent/tests/<test-name>/<file>, ...
Output: general-coding-agent/results/<version>/<test-name>/ (file1, file2, ...)
```

- All paths include `general-coding-agent/` prefix so outputs stay inside the project.
- Output: single directory path; list specific files in parentheses.
- Version in Output is provided at test time.

---

## Core File Roles

| File | Deploys To | Role |
|------|-----------|------|
| `core/agent.md` | `~/.cursor/commands/agent.md` | Orchestrator: plans, delegates, manages quality, maintains workspace, selects models. |
| `core/subagents/executor.md` | `~/.cursor/agents/executor.md` | General-purpose implementation. |
| `core/subagents/designer.md` | `~/.cursor/agents/designer.md` | Visual deliverables (PDF, web, slides). |
| `core/subagents/debugger.md` | `~/.cursor/agents/debugger.md` | Targeted fixes within scoped file list. |
| `core/subagents/qa-specialist.md` | `~/.cursor/agents/qa-specialist.md` | Read-only output quality inspection. |
| `core/subagents/verifier.md` | `~/.cursor/agents/verifier.md` | Per-item PASS/FAIL checks. |
| `core/subagents/file-explorer.md` | `~/.cursor/agents/file-explorer.md` | Document extraction and organization. |

---

## Agent Design Principles

Follow these when modifying any file in `core/`.

1. **Description balance.** Each feature's description length should be proportional to its importance. An over-detailed single feature drowns out other rules -- the agent optimizes for what's most prominent in its prompt. Keep all sections balanced in weight.

2. **Cross-file consistency.** After any edit to `agent.md`, verify:
   - `<role>` aligns with `<rules>` (no contradictions).
   - `<team>` table descriptions match each subagent's YAML `description` field.
   - Rules don't contradict each other (e.g., delegation rules vs. direct execution rules).
   - `<workflow>` references valid rule numbers and section names.
   After editing subagent files, verify their YAML description matches `agent.md`'s `<team>` table.
   **Report issues immediately** -- do not defer consistency checks to later.

3. **Surgical edits.** Only modify what the requirement asks for. Don't refactor adjacent sections. If you find other issues while editing, report them -- don't silently fix.

4. **Compatibility check.** Before adding new features, check how they interact with existing features. New mechanisms must not break or contradict existing ones. Read the full `<rules>` and `<workflow>` sections before making changes.

5. **Requirements-first.** Before implementing changes to `core/`, ensure requirements are captured in `current/requirements/<feature>.md`. If requirements evolve during implementation, update the requirements file to match the final agreed design.

---

## Iterations

```
iterations/
└── v1/
    ├── requirements/
    │   ├── cost-aware-and-model-selection.md
    │   └── planning-reflection-filesystem.md
    ├── problems.md
    ├── code_review.md
    ├── human_feedback.md
    ├── cv2-homework3_self_reflection.md
    ├── cv2-homework3_plan.md
    └── files/
```

**Requirements** (`requirements/`) — agreed-upon feature specs for this version's changes. Written before or during implementation; updated to match final design if requirements evolved. One file per feature.

**Problems** (`problems.md`) — consolidated list of issues found (from code review, self-reflection, human feedback). Prioritized by severity (P0-P3).

**Code review** (`code_review.md`) — structured review of agent definitions, identifying design issues and gaps.

**Human feedback** (`human_feedback.md`) — user observations from test runs.

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

## Version Transition

When the user says "commit to next version" (or similar), run this procedure. The user provides the target version number (e.g., v2).

### Phase 1: Finalize current version workspace

- [ ] **Requirements sync.** Check `current/requirements/` for each feature changed in this version:
  - File missing → create it from the implemented design (what was agreed on, not the raw conversation).
  - File exists → verify it matches the actual implementation. If requirements evolved during implementation, update the file to reflect the final agreed design.
- [ ] **Workspace completeness.** Ensure `current/` contains relevant artifacts: `problems.md`, `code_review.md`, `human_feedback.md`, self-reflection and plan files as applicable.

### Phase 2: Consistency check

Run the cross-file consistency check (see Agent Design Principles):
- [ ] `<role>` aligns with `<rules>`.
- [ ] `<team>` table descriptions match each subagent's YAML `description` field.
- [ ] Rules don't contradict each other.
- [ ] `<workflow>` references valid rule numbers and section names.
- [ ] Never rename XML tags in `agent.md` (`<role>`, `<team>`, `<workspace>`, `<rules>`, `<workflow>`) without checking all references.
- Report any issues before proceeding.

### Phase 3: Deploy and archive

```bash
./scripts/deploy.sh --archive
```

This deploys `core/` to Cursor AND archives `core/` to `current/files/core/` (snapshot of this version's agent definitions). Verify deployed files match source with diff.

### Phase 4: Version transition

```bash
mkdir -p iterations/<new-version>/requirements iterations/<new-version>/files
rm current && ln -s iterations/<new-version> current
```

Append a version entry to `history.md` (never modify past entries). Include: what changed, why, which files were modified, which test cases validated it.

### Phase 5: Commit (if requested)

```bash
git add -A && git commit -m "v<N>: <short summary>" && git push
```

### Core file edit rules (apply during any version)

- If a subagent's behavior changed: update BOTH the subagent `.md` file AND its row in the `<team>` table in `agent.md` (must stay in sync).
- If adding a new subagent: create `core/subagents/<name>.md` + add `<team>` row (`deploy.sh` auto-discovers `*.md`).
- If removing a subagent: delete the file + remove its `<team>` row.
