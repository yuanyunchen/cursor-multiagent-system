# Agent Development Workspace Guide

Read before changing the Cursor Multiagent System.

---

## Workspace Structure

```
cursor-multiagent-system/
├── core/                  # Source of truth for agents
│   ├── agent.md           #   Orchestrator -> ~/.cursor/commands/
│   └── subagents/*.md     #   Subagents    -> ~/.cursor/agents/
├── skills/<name>/         # Skills         -> ~/.cursor/skills/<name>/
├── scripts/deploy.sh      # Sync core/ + skills/ to Cursor; --archive snapshots
├── tests/<test-name>/     # prompt.txt + input files
├── iterations/
│   ├── current/           # Active iteration (renamed to v<N>/ on transition)
│   │   ├── requirements/<feature>.md
│   │   ├── problems.md, code_review.md, human_feedback.md
│   │   ├── <test-name>_self_reflection.md, <test-name>_plan.md
│   │   └── files/{core,skills,scripts}/   # Full versioned snapshot
│   └── v<N>/              # Past iterations
├── results/current/<test-name>/   # Renamed to v<N>/ on transition
├── current -> iterations/current  # Symlink
├── history.md             # Append-only version log
├── llm.md, README.md, .gitignore
```

Each subagent and skill owns its own description (subagent YAML + `SKILL.md`); treat those as the single source of truth for capabilities. Don't duplicate that here.

**Tracked in git:** `core/`, `skills/`, `scripts/`, `README.md`, `history.md`, `llm.md`, `.gitignore`. Everything else (`tests/`, `iterations/`, `results/`) stays local.

---

## Naming Conventions

All directories and `.md` files use lowercase, hyphen-separated names. Non-obvious patterns:

| Item | Pattern | Example |
|------|---------|---------|
| Session | `<version>_<test-name>_<model>` | `v1.2_aml-assignment1_gpt-5.4` |
| Iteration dir | `current/` while active, `v<N>/` after transition | `iterations/v1.5/` |
| Reflection / plan | `<test-name>_self_reflection.md`, `<test-name>_plan.md` | `cv2-homework3_plan.md` |

**`prompt.txt`** in each test:

```
Task: <one-sentence description>
Input: cursor-multiagent-system/tests/<test-name>/<file>, ...
Output: cursor-multiagent-system/results/current/<test-name>/ (file1, ...)
```

All paths include the `cursor-multiagent-system/` prefix; output always writes to `results/current/` (renamed on version transition).

---

## Agent Design Principles

Apply when modifying anything in `core/` or `skills/`.

1. **Description balance.** Section length should track section importance. An over-detailed feature drowns out the rest — the model optimizes for whatever is most prominent.
2. **Surgical edits.** Change only what the requirement asks for. Report adjacent issues; don't silently fix.
3. **Compatibility check.** Before adding a feature, read the relevant `<rules>` and `<workflow>` so the new mechanism doesn't contradict existing ones.
4. **Single dispatch contract.** `agent.md`'s `<task_format>` is the only task interface. Subagent-specific needs are added as optional fields on `<task_format>`, not parallel formats. Keep `<output>` semantically structured (named child fields, not free-form blobs).
5. **Cross-file consistency** (run after every edit to `core/`):
   - `<role>` ↔ `<rules>` ↔ `<workflow>` are mutually consistent (no rule the workflow violates, no workflow step the role forbids).
   - `<team>` rows match each subagent's YAML `description`, and only reference real built-ins / tools / subagent types.
   - `<task_format>` field usage matches how each subagent actually reads the task.
   - `<workflow>` references valid rule numbers and section names.
   - Workspace conventions (e.g. `uploads/`, `.workspace`) are described identically wherever they appear.
   - `README.md` reflects any change in public-facing workflow, capabilities, or workspace conventions.
   - **Never rename XML tags** in `agent.md` without auditing every reference.
   Report violations immediately — do not defer.
6. **Requirements-first.** Capture intent in `iterations/current/requirements/<feature>.md` before or during implementation; update it if the design evolves.

---

## Iterations

Per-version workspace under `iterations/v<N>/`:

- **`requirements/<feature>.md`** — agreed-upon spec, one file per feature; reflects final design.
- **`problems.md`** — consolidated issues, severity P0–P3.
- **`code_review.md`** — review findings on agent definitions.
- **`human_feedback.md`** — user observations from runs.
- **`<test>_self_reflection.md`** — actual vs. expected execution: flow table, issues (severity / rule / impact), root cause, proposed fixes referencing concrete sections in `core/`.
- **`<test>_plan.md`** — translates reflection into edits: issues to address (linked to reflection IDs), per-file changes (file, section, current, proposed, rationale), test plan.
- **`files/{core,skills,scripts}/`** — full snapshot of source-of-truth dirs at this version (produced by `deploy.sh --archive`). Every version transition must produce a complete snapshot so any past version can be reconstructed.

---

## Git & Versioning

**Single branch `main`.** Commit directly. Feature branches only for high-risk experiments (`<scope>-<topic>`); merge and delete in the same session. Never force-push or delete `main` (branch protection blocks it; do not work around). External contributors use PRs (1 review required); admins bypass via `enforce_admins: false`.

**Scheme** `major.minor.patch`:
- Major (v2 → v3): architectural redesign / breaking changes.
- Minor (v2.1 → v2.2): new features, workflow / role redesign. Use the user-specified version when given; otherwise infer from scope.
- Patch (v2.1.1 → v2.1.2): every commit auto-increments; look up latest in `history.md`.

**Every commit:**
1. `./scripts/deploy.sh` (sync to Cursor before committing — runtime must match source).
2. Append entry to `history.md` (date, summary, changes, files).
3. `git commit -m "v<N>: <summary>"` and `git push origin main`.
4. Report old → new version with change summary.

---

## Version Transition

Triggered by "commit to next version" (or similar). Use the user-specified version when given; otherwise infer.

**Phase 1 — Finalize current workspace.** Each feature changed in this version has an up-to-date `requirements/<feature>.md` matching the final design (create if missing). Confirm `problems.md`, `code_review.md`, `human_feedback.md`, and reflection / plan files are present where applicable.

**Phase 2 — Consistency check.** Run the cross-file consistency check from Agent Design Principle 5. Report any issues before proceeding.

**Phase 3 — Deploy and archive.**

```bash
./scripts/deploy.sh --archive
```

Deploys `core/`, `skills/`, `scripts/` to Cursor and snapshots all three into `iterations/current/files/{core,skills,scripts}/`. Diff to verify deployed files match source.

**Phase 4 — Roll over.**

```bash
mv iterations/current iterations/v<N>
mv results/current   results/v<N>
mkdir -p iterations/current/requirements iterations/current/files
```

The `current -> iterations/current` symlink is unchanged. Append a version entry to `history.md` (never modify past entries): what changed, why, files modified, validating tests.

**Phase 5 — Commit (if requested).** Follow the commit protocol above (deploy → history → commit → push).

---

## Core Edit Rules

- Subagent behavior changed → update both `core/subagents/<name>.md` and its row in the `<team>` table in `agent.md`.
- Add a subagent → create `core/subagents/<name>.md` and add a `<team>` row. `deploy.sh` auto-discovers `*.md`.
- Remove a subagent → delete the file and the `<team>` row.
