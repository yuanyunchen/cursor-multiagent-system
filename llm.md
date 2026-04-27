# Agent Development Workspace Guide

Read this document before making any changes to the Cursor Multiagent System.

---

## Workspace Structure

```
cursor-multiagent-system/
├── core/                         # Source of truth — agent definitions
│   ├── agent.md                  #   Orchestrator (deploys to ~/.cursor/commands/)
│   └── subagents/                #   Subagent definitions (deploy to ~/.cursor/agents/)
│       ├── debugger.md
│       ├── report-writer.md
│       ├── frontend-engineer.md
│       ├── executor.md
│       ├── file-extractor.md
│       ├── qa-specialist.md
│       └── verifier.md
├── skills/                       # Skill files referenced by subagents (deploy to ~/.cursor/skills/)
│   ├── file-content-extraction/  #   PDF/DOCX/PPTX extraction instructions
│   │   └── SKILL.md
│   ├── webpage-content-extraction/ # Web page extraction instructions
│   │   └── SKILL.md
│   ├── write-report/              #   LaTeX PDF report writing standards + template cache
│   │   ├── SKILL.md              #     content architecture + local template selection
│   │   ├── scripts/              #     build.py, validate_pdf.py, longtable_to_tabular.lua
│   │   └── templates/            #     preprocessed local starters + manifest.json
│   ├── pptx/                     #   Slide creation/editing skill (full suite)
│   ├── frontend-design/          #   Aesthetic direction, typography, motion, layout (frontend-engineer)
│   │   └── SKILL.md
│   ├── theme-factory/            #   Color palette + font pairing themes (frontend-engineer)
│   │   ├── SKILL.md
│   │   ├── theme-showcase.pdf
│   │   └── themes/
│   ├── web-artifacts-builder/    #   React + Tailwind + shadcn artifact scaffold (frontend-engineer)
│   │   ├── SKILL.md
│   │   └── scripts/              #     init-artifact.sh, bundle-artifact.sh
│   └── webapp-testing/           #   Playwright-based render/test/console capture (frontend-engineer)
│       ├── SKILL.md
│       ├── scripts/              #     with_server.py
│       └── examples/
├── scripts/                      # Utility scripts
│   └── deploy.sh                 #   Sync core/, skills/ to Cursor
├── tests/                        # Test cases for evaluating agent behavior
│   └── <test-name>/
│       ├── prompt.txt            #   Agent command (Task / Input / Output)
│       └── <input-files>         #   PDF, PPTX, images, code, etc.
├── iterations/                   # Development logs organized by version
│   ├── current/                  #   Active iteration (renamed to <version>/ on transition)
│   │   ├── requirements/         #   Feature requirements for this version
│   │   │   └── <feature-name>.md
│   │   ├── problems.md           #   Consolidated issue list
│   │   ├── code_review.md        #   Code review findings
│   │   ├── human_feedback.md     #   User feedback from test runs
│   │   ├── <test-name>_self_reflection.md
│   │   ├── <test-name>_plan.md
│   │   └── files/                #   Archived core/ snapshot, diffs, screenshots, logs
│   │       └── core/             #   Snapshot of core/ at this version
│   └── <version>/                #   Past iterations (archived from current/)
├── results/                      # Agent output from test runs
│   └── current/                 #   Active test run output (renamed to <version>/ on version transition)
│       └── <test-name>/
│           └── <output-files>
├── current -> iterations/current    # Symlink to active iteration workspace
├── history.md                    # Version history (append-only)
├── llm.md                        # This file
├── README.md                     # Public-facing documentation
└── .gitignore
```

### What Goes to GitHub

| Tracked | Not tracked |
|---------|-------------|
| `core/`, `skills/`, `scripts/`, `README.md`, `history.md`, `llm.md`, `.gitignore` | `tests/`, `iterations/`, `results/` |

---

## Naming Conventions

| Item | Rule | Example |
|------|------|---------|
| Directories | lowercase, hyphen-separated | `cv2-homework3` |
| Agent files | lowercase, hyphen-separated `.md` | `qa-specialist.md` |
| Test folders | descriptive, hyphen-separated | `aml-assignment1` |
| Results folders | `current/<test-name>/` (renamed to `<version>/` on transition) | `cursor-multiagent-system/results/current/aml-assignment1/` |
| Session name | `<version>_<test-name>_<model>` | `v1.2_aml-assignment1_gpt-5.4` |
| Iteration dirs | `current/` while active, `v<N>/` after transition | `iterations/current/`, `iterations/v1.5/` |
| Self-reflection files | `<test-name>_self_reflection.md` | `cv2-homework3_self_reflection.md` |
| Plan files | `<test-name>_plan.md` | `cv2-homework3_plan.md` |

### prompt.txt Format

```
Task: <one-sentence description>
Input: cursor-multiagent-system/tests/<test-name>/<file>, ...
Output: cursor-multiagent-system/results/current/<test-name>/ (file1, file2, ...)
```

- All paths include `cursor-multiagent-system/` prefix so outputs stay inside the project.
- Output always uses `results/current/`. On version transition, `current/` is renamed to `<version>/`.

---

## Core File Roles

| File | Deploys To | Role |
|------|-----------|------|
| `core/agent.md` | `~/.cursor/commands/agent.md` | Orchestrator: plans, delegates, manages quality, maintains workspace, selects models. |
| `core/subagents/executor.md` | `~/.cursor/agents/executor.md` | General-purpose implementation. |
| `core/subagents/report-writer.md` | `~/.cursor/agents/report-writer.md` | Professional LaTeX PDF reports only. Uses `write-report` for content standards, template cache/update, LaTeX build, and QA. Owns content organization plus formatting; returns `NEEDS_MORE_CONTEXT` when inputs are insufficient. |
| `core/subagents/frontend-engineer.md` | `~/.cursor/agents/frontend-engineer.md` | Web-based deliverables: HTML reports/posters, static webpages, dashboards, and interactive apps. Uses `~/.cursor/skills/frontend-design`, `theme-factory`, `web-artifacts-builder` when justified, and `webapp-testing` for dynamic validation. Standard render/test-inspect-fix-cleanup QA loop writes `frontend_qa.md`; loop artifacts are removed from final deliverables. |
| `core/subagents/debugger.md` | `~/.cursor/agents/debugger.md` | Targeted fixes within scoped file list. |
| `core/subagents/qa-specialist.md` | `~/.cursor/agents/qa-specialist.md` | End-to-end output inspector (black-box, never reads code). |
| `core/subagents/verifier.md` | `~/.cursor/agents/verifier.md` | Comprehensive code reviewer; fixes minor issues, reports major ones. |
| `core/subagents/file-extractor.md` | `~/.cursor/agents/file-extractor.md` | Document & web page content extraction. |
| `skills/file-content-extraction/` | `~/.cursor/skills/file-content-extraction/` | PDF/DOCX/PPTX extraction instructions for file-extractor. |
| `skills/webpage-content-extraction/` | `~/.cursor/skills/webpage-content-extraction/` | Web page extraction instructions for file-extractor. |
| `skills/write-report/` | `~/.cursor/skills/write-report/` | Report writing standards, scenario routing, template cache/update rules, build scripts, and LaTeX templates for report-writer. |
| `skills/pptx/` | `~/.cursor/skills/pptx/` | Slide creation/editing skill. |
| `skills/frontend-design/` | `~/.cursor/skills/frontend-design/` | Aesthetic direction guidelines for frontend-engineer, including HTML reports/posters and web interfaces. |
| `skills/theme-factory/` | `~/.cursor/skills/theme-factory/` | Color/font theme presets (10 themes) for frontend-engineer. |
| `skills/web-artifacts-builder/` | `~/.cursor/skills/web-artifacts-builder/` | React + Tailwind + shadcn artifact scaffold and bundling for frontend-engineer. |
| `skills/webapp-testing/` | `~/.cursor/skills/webapp-testing/` | Playwright-based webapp testing toolkit for frontend-engineer. |
| `skills/file-content-extraction/extract_doc.py` | `~/.cursor/skills/file-content-extraction/extract_doc.py` | Document content + figure extraction script. |

---

## Agent Design Principles

Follow these when modifying any file in `core/`.

1. **Description balance.** Each feature's description length should be proportional to its importance. An over-detailed single feature drowns out other rules -- the agent optimizes for what's most prominent in its prompt. Keep all sections balanced in weight.

2. **Cross-file consistency.** After any edit to `agent.md`, verify:
   - `<role>` aligns with `<rules>` (no contradictions).
   - `<role>` aligns with `<workflow>` (the workflow must not require actions the role forbids).
   - `<team>` table descriptions match each subagent's YAML `description` field.
   - `<team>` only lists built-ins / tools / subagent types that actually exist in the runtime.
   - `<team>` I/O expectations match how each subagent actually reads `<task>` fields.
   - `README.md` matches `agent.md` on public-facing workflow, built-in names, and workspace behavior.
   - `uploads/` behavior is described consistently wherever `.workspace` is documented.
   - Rules don't contradict each other (e.g., delegation rules vs. direct execution rules).
   - `<workflow>` references valid rule numbers and section names.
   - `<task_format>` is the single dispatch contract; subagent docs must not invent incompatible input formats.
   After editing subagent files, verify their YAML description matches `agent.md`'s `<team>` table.
   **Report issues immediately** -- do not defer consistency checks to later.

3. **Surgical edits.** Only modify what the requirement asks for. Don't refactor adjacent sections. If you find other issues while editing, report them -- don't silently fix.

4. **Compatibility check.** Before adding new features, check how they interact with existing features. New mechanisms must not break or contradict existing ones. Read the full `<rules>` and `<workflow>` sections before making changes.

5. **Single task protocol.** `agent.md`'s `<task_format>` is the only task dispatch contract. If a subagent needs special control fields, add them as optional fields to `<task_format>` and document how that subagent uses them. Do not create parallel ad hoc formats in subagent files. Keep `<output>` semantically structured: use named child fields rather than one overloaded free-form blob.

6. **Public docs stay aligned.** When a change affects capabilities, workflow, built-in names, or workspace conventions, update `README.md` in the same edit set unless it is intentionally internal-only.

7. **Requirements-first.** Before implementing changes to `core/`, ensure requirements are captured in `current/requirements/<feature>.md`. If requirements evolve during implementation, update the requirements file to match the final agreed design.

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

## Git Branch Policy

**Single branch: `main`.** Commit directly to `main` for all normal work — fixes, iterations, version bumps, documentation. No per-change feature branches.

- **Owner / admin push directly to `main`.** Branch protection is configured with `enforce_admins: false`, so admins bypass the PR review requirement. Force-push and branch deletion on `main` remain blocked and must not be circumvented.
- **External contributors use PRs.** Protection still requires 1 approving review before merge. An admin reviews and merges on the contributor's behalf.
- **Feature branches are reserved for high-risk work only.** Long-running experiments or anything that might leave `main` broken. Name `<scope>-<topic>` (e.g., `experiment-parallel-agents`), merge back as soon as the work stabilizes, and delete both locally (`git branch -d`) and on the remote (`git push origin --delete <branch>`) in the same session — no lingering branches.
- **Never force-push `main`. Never delete `main`.** These are blocked by protection; do not attempt workarounds.

This removes PR-ceremony overhead for solo work and keeps history linear.

## Versioning

**Scheme:** `major.minor.patch` (e.g., v2.1.3)
- **Major** (v2 -> v3): architectural redesign, breaking changes.
- **Minor** (v2.1 -> v2.2): new features, workflow changes, role redesigns. If the user specifies the version number, use it. Otherwise, infer the appropriate next version from the scope of changes.
- **Patch** (v2.1.1 -> v2.1.2): every git commit auto-increments patch. Look up the latest version in `history.md` and bump.

**Commit protocol:** Every commit must:
1. Deploy first (`./scripts/deploy.sh`)
2. Append a version entry to `history.md` (date, one-line summary, changes, files modified)
3. Commit with message `v<N>: <short summary>`
4. Push directly to `main` (`git push origin main`)
5. Report to user: old version -> new version + change summary

## Version Transition

When the user says "commit to next version" (or similar), always run the full transition procedure below. Use the user-provided target version number when given; otherwise, infer the appropriate next version from the versioning scheme above.

### Phase 1: Finalize current version workspace

- [ ] **Requirements sync.** Check `current/requirements/` for each feature changed in this version:
  - File missing → create it from the implemented design (what was agreed on, not the raw conversation).
  - File exists → verify it matches the actual implementation. If requirements evolved during implementation, update the file to reflect the final agreed design.
- [ ] **Workspace completeness.** Ensure `current/` contains relevant artifacts: `problems.md`, `code_review.md`, `human_feedback.md`, self-reflection and plan files as applicable.

### Phase 2: Consistency check

Run the cross-file consistency check (see Agent Design Principles):
- [ ] `<role>` aligns with `<rules>`.
- [ ] `<role>` aligns with `<workflow>`.
- [ ] `<team>` table descriptions match each subagent's YAML `description` field.
- [ ] `<team>` only references built-ins / tools / subagent types that actually exist in the runtime.
- [ ] `<team>` I/O expectations match how each subagent actually reads `<task>` fields.
- [ ] `README.md` matches `agent.md` on workflow, built-in names, and workspace behavior.
- [ ] `uploads/` behavior is described consistently wherever `.workspace` is documented.
- [ ] Rules don't contradict each other.
- [ ] `<workflow>` references valid rule numbers and section names.
- [ ] `<task_format>` remains the single dispatch contract across `agent.md` and all subagent docs.
- [ ] Never rename XML tags in `agent.md` (`<role>`, `<team>`, `<workspace>`, `<rules>`, `<workflow>`) without checking all references.
- Report any issues before proceeding.

### Phase 3: Deploy and archive

```bash
./scripts/deploy.sh --archive
```

This deploys `core/`, `skills/`, and `scripts/` to Cursor AND archives `core/` to `current/files/core/` (snapshot of this version's agent definitions). Verify deployed files match source with diff.

### Phase 4: Version transition

Choose the version number from the user instruction when available; otherwise infer it from the scope of changes. Then rename both `iterations/current` and `results/current` to that version. A new empty `iterations/current` is created for the next development cycle.

```bash
# Archive current iteration and results under the chosen version
mv iterations/current iterations/<version>
mv results/current results/<version>

# Set up next iteration (stays as "current" — no version number assigned yet)
mkdir -p iterations/current/requirements iterations/current/files
# Symlink unchanged: current -> iterations/current
```

Append a version entry to `history.md` (never modify past entries). Include: what changed, why, which files were modified, which test cases validated it.

### Phase 5: Commit (if requested)

**Always deploy before committing** — run `deploy.sh` first to ensure Cursor runtime matches the repo source.

```bash
./scripts/deploy.sh
git add -A && git commit -m "v<N>: <short summary>" && git push
```

### Core file edit rules (apply during any version)

- If a subagent's behavior changed: update BOTH the subagent `.md` file AND its row in the `<team>` table in `agent.md` (must stay in sync).
- If adding a new subagent: create `core/subagents/<name>.md` + add `<team>` row (`deploy.sh` auto-discovers `*.md`).
- If removing a subagent: delete the file + remove its `<team>` row.
