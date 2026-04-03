# Version History

## v1 (2026-03-10)

Initial release of the multi-agent orchestration system for Cursor IDE.

### Architecture

- **Orchestrator** (`core/agent.md`): Senior tech-lead agent that owns planning, delegation, and quality management. Never writes code or runs commands directly. Classifies incoming tasks as S/M/L and follows size-appropriate workflows.
- **6 custom subagents** (`core/subagents/`): Each has a single responsibility, strict scope rules, and a standardized output format.
- **3 built-in agents** (Cursor-native): `explore` (codebase search), `shell` (command execution), `browser-use` (web automation).

### Subagents

| Agent | File | Role |
|-------|------|------|
| executor | `executor.md` | General-purpose implementation. Receives scoped tasks, executes precisely, flags ambiguity. Minimal-diff principle. |
| designer | `designer.md` | Visual deliverable creator. Takes markdown content + figures, produces PDF (LaTeX or HTML), web pages, or slides. Never alters content. Runs build-validate-fix loop (max 3 iterations). |
| debugger | `debugger.md` | Targeted fixer. Receives issue list + `<allowed_files>` scope. Applies minimal fixes, reports out-of-scope observations. |
| qa-specialist | `qa-specialist.md` | Read-only output quality inspector. Two modes: Full (comprehensive, define own validation dimensions) and Lightweight (quick sanity check). Classifies findings as blockers vs. suggestions. |
| verifier | `verifier.md` | Fast per-item PASS/FAIL checker. Receives explicit checklist + criteria. Can inspect code, logs, outputs, diffs. One-line evidence per item. |
| file-extractor | `file-extractor.md` | Document & web page content extraction. Two-phase: extract (via file-content-extraction / webpage-content-extraction skills) then organize (restructure, integrate figures, remove noise). Handles PDF, DOCX, PPTX, URLs. |

### Quality Control

- **QA closed loop**: QA Specialist (find) -> Debugger (fix, scoped) -> Verifier (confirm) -> re-QA. Max 3 rounds, then escalate to user.
- **Checkpoint validation**: Core modules get Verifier checks mid-execution; critical modules escalate to full QA.
- **Mandatory final QA**: Nothing ships without a passed full-mode QA Specialist round.
- **Blocker vs. suggestion**: QA reports distinguish must-fix blockers from optional suggestions (HIGH/MEDIUM priority).

### Workflow

- **Task sizing**: S (single file, <10 lines), M (clear scope, few files), L (multi-file, architecture needed). Each size has a defined flow.
- **S**: Dispatch -> scan -> reply.
- **M**: Plan -> user confirms -> Execute -> Validate -> Iterate -> Deliver.
- **L**: Understand -> Architect -> user confirms -> Execute in parallel rounds (with checkpoints) -> Final Validate -> Iterate -> Deliver.
- **Iteration control**: Structured review after each round (improved, gap analysis, next plan, decision). Hard cap of 5 rounds. User override takes precedence.

### Dispatch Model

- **Parallel by default**: Independent tasks always dispatched concurrently. Sequential dispatch of independent tasks is explicitly prohibited.
- **Full context per task**: Subagents have zero memory across dispatches. Every task includes all file paths, specs, architecture decisions, and acceptance criteria.
- **Model selection**: Each dispatch chooses `fast` (cheaper, sufficient for well-scoped tasks) or `default` (stronger reasoning, for complex tasks). Per-role defaults defined.
- **Task format**: Standardized XML block with id, type, title, description, files, context, acceptance criteria.

### Tested On

- CV2 Homework 3: Structure from Motion pipeline + PDF report (L-size task)

## v1.3 (2026-03-12)

Workflow restructure and simplification.

### Changes

- **Removed S/M/L classification.** Single unified workflow for all tasks. Workspace always created.
- **Flattened plan directory.** `plan_v0.md` → `initial_plan.md`, `plan.md` — both directly under `.workspace/` (no `plan/` subdirectory).
- **Simplified plan definition.** Removed HOW-to-write guidance to avoid conflicting with workflow. Plan defines: modules and workflow, agent and model assignments, quality checkpoints.
- **Merged quality pipeline rule into workflow.** Rule 2 ("Own quality management") removed from rules; its content (Verifier → Debug → QA → Designer pipeline, escalation, no hands-on QC) merged into workflow Execute step.
- **Workflow steps name subagents.** Each step explicitly states which agents are involved.
- **Split document management and dispatch context.** Old Rule 5 split into Rule 4 (document management) and Rule 5 (dispatch context).
- **Consistency fixes.** Updated YAML descriptions for verifier, qa-specialist, debugger, and designer team table entry to match v1.2 behavioral changes.

### Files Modified

- `core/agent.md` — major restructure (276 → 276 lines, but significantly reorganized)
- `core/subagents/qa-specialist.md` — fixed outdated standards path, updated YAML description
- `core/subagents/verifier.md` — updated YAML description (can fix, holistic scan)
- `core/subagents/debugger.md` — updated YAML description (triggered by Verifier or QA)

### Tested On

- CV2 Homework 3: Structure from Motion (v1.3-plan-mode, v1.3-gpt variants)

## v1.5 (2026-03-12)

Agent role redefinition, quality pipeline overhaul, and documentation standardization.

### Changes

- **Orchestrator role strengthened.** Sole focus on high-level planning, modular decomposition, delegation, and quality management. Never looks at code. New Rule 5: Context and document management — orchestrator tracks `index.md` as a document registry, encapsulates reused context, minimizes subagent file reads.
- **Designer renamed to report-writer.** Writes content and produces deliverables directly in target format (LaTeX/HTML/PPTX) — no markdown intermediate. Handles writing style, terminology, and domain conventions. Default model: inherit.
- **Verifier redesigned.** From checklist ticker to comprehensive code reviewer. Input: requirements + code scope + optional standards. Reviews holistically, fixes minor issues directly, reports major issues with feedback and optimization suggestions. Problem-focused documentation with requirements check.
- **QA Specialist redesigned.** Strict black-box tester — never reads code, only inspects deliverable output. Defines own acceptance criteria. Every task requires at least one Full mode QA.
- **Plan structure formalized.** Task analysis → modules (requirements + pipeline) → overall pipeline. Each module pipeline specifies agent type + model, task scope, and execution mode (sequential/parallel/loop).
- **Module execution loop.** Execute → Verify → QA → Reflect, max 3 rounds per module. Core modules use inherit for both verifier and QA.
- **Subagent documentation standardized.** All subagents write detailed reports to `.workspace/documents/`; messages to orchestrator are concise summaries. All subagents have "minimize file reads" rule.
- **Executor role enhanced.** Senior engineer identity. "Always seek the better solution" rule. Minimal change for existing code, full architectural freedom for new modules.
- **Model selection refined.** Fast as default, inherit for core modules and retries. Full mode available on user request.
- **Workspace simplified.** Removed `execution_log.md` and `standards/` directory. Results default to `results/current/`.

### Files Modified

- `core/agent.md` — major: role, team table, rules (new Rule 5), workflow (plan structure, execution loop, Final QA), workspace definitions
- `core/subagents/executor.md` — role definition, documentation structure, rules (seek better solution, minimize file reads, minimal change clarification)
- `core/subagents/verifier.md` — complete redesign: comprehensive code review, fix minor/report major, problem-focused documentation
- `core/subagents/qa-specialist.md` — redesign: black-box tester, own criteria, minimize file reads
- `core/subagents/debugger.md` — added documentation section, minimize file reads rule
- `core/subagents/report-writer.md` — new file (replaced designer.md): content writing + direct formatting
- `core/subagents/file-extractor.md` — renamed from file-explorer, scope clarified for web pages
- `llm.md` — results/current path, version transition, designer→report-writer rename
- All `prompt.txt` files — output path updated to `results/current/`

### Tested On

- CV2 Homework 4 (results/v1.5/cv2-homework4, cv2-homework4-kimi)

## v2 (2026-03-15)

Self-contained repository: all skills, scripts, and templates internalized. Extraction quality improvements.

### Changes

- **Skills and scripts internalized.** All external dependencies (`~/.cursor/skills/`, `~/.cursor/scripts/`) copied into the project under `skills/` and `scripts/`. The project repo is now the single source of truth; `deploy.sh` syncs to `~/.cursor/` for runtime.
- **`deploy.sh` expanded.** Now syncs `skills/` directories to `~/.cursor/skills/` via `rsync` in addition to `core/` agent definitions.
- **`designer-subagent` renamed to `report-builder`.** Clearer name for the report build tools (scripts, LaTeX templates, HTML styles).
- **`extract_doc.py` relocated.** Moved from `scripts/` to `skills/file-content-extraction/` (co-located with its skill).
- **PDF extraction improved.** Template image filtering: images appearing on 3+ pages classified as decorative (slide backgrounds, logos) and removed. Decorative table filtering: tables with >70% empty cells or fully redundant content removed.
- **File-extractor workflow updated.** Step 3 renamed from "Organize" to "Fix & Organize" with two explicit categories: format fixes (merged words, broken lines, artifacts, page headers) and structural organization (headings, figure placement). Rule 1 rewritten from "Preserve ALL original content" to "Fix format, preserve content."
- **`llm.md` updated.** Workspace structure includes `skills/` tree. Tracked files table includes `skills/`. Core File Roles table expanded with skill and script entries.

### Files Modified

- `skills/` — new directory: `file-content-extraction/`, `webpage-content-extraction/`, `report-builder/`, `pptx/`
- `scripts/deploy.sh` — expanded with skills sync
- `skills/file-content-extraction/extract_doc.py` — template image filtering, decorative table filtering
- `core/subagents/file-extractor.md` — Fix & Organize workflow, format repair rules
- `core/subagents/report-writer.md` — `designer-subagent` -> `report-builder` path updates
- `skills/file-content-extraction/SKILL.md` — `extract_doc.py` path update
- `skills/webpage-content-extraction/SKILL.md` — `extract_doc.py` path update
- `llm.md` — workspace structure, tracked files, core file roles

### Tested On

- CV2 Homework 4 v2 (results/v2/cv2-homework4-kimi, cv2-homework4-kimi-v2)
- AML Lecture 2 PDF extraction (file-explorer/results/v1.5_aml_lecture2)

## v2.1 (2026-03-14)

Workflow simplification: tiered quality pipeline and model selection removal.

### Changes

- **Tiered module execution.** Replaced the single Execute -> Verify -> QA loop with two distinct paths:
  - **Routine modules:** executor only, then reflect. No verifier, no QA.
  - **Core modules:** executor -> verifier -> qa-specialist (Full mode), loop max 3 rounds.
- **Final review requires both verifier and QA.** Step 4 now mandates verifier on all final code + qa-specialist (Full mode) on all deliverables before delivery. Previously only QA was mandatory.
- **Model selection removed.** Entire model selection block (parameter docs, fast/inherit guidance, Full mode directive, role defaults table) removed from `agent.md`. All subagents now use system default (inherit). Archived block saved to `history.md`.
- **Plan example updated.** Now shows both a routine module (executor only) and a core module (full loop) to illustrate the two paths. Model annotations removed from pipeline specs.
- **QA Specialist description updated.** Removed "Use after Verifier confirms code is clean" — QA is no longer always preceded by verifier.

### Files Modified

- `core/agent.md` — workflow steps 3-4 rewritten, model selection block removed, plan example updated (220 -> 197 lines)
- `core/subagents/qa-specialist.md` — YAML description updated
- `history.md` — archived model selection block, v2.1 entry

## v2.1.1 (2026-03-14)

Add back simplified model selection; enforce deploy-before-commit.

### Changes

- **Model selection restored (simplified).** Two-line version: inherit for quality-critical work (core modules, verifier, QA, report-writer), fast for routine execution (commands, config, file reads).
- **Deploy-before-commit rule.** Added to `llm.md` Phase 5: always run `deploy.sh` before `git commit`.

### Files Modified

- `core/agent.md` — model selection block added back (simplified)
- `llm.md` — Phase 5 updated with deploy-before-commit

## v2.1.2 (2026-03-14)

Versioning scheme and commit protocol.

### Changes

- **Versioning scheme defined.** `major.minor.patch` — major for architecture, minor for features (user-assigned), patch auto-increments per commit.
- **Commit protocol formalized.** Every commit: deploy -> append `history.md` entry -> commit -> report (old version -> new version + changes).
- **Retroactive patch version.** Added v2.1.1 entry for the previous unversioned commit.

### Files Modified

- `llm.md` — new "Versioning" section with scheme + commit protocol
- `history.md` — v2.1.1 and v2.1.2 entries added

---

## Archived: Model Selection (removed in v2.1, restored simplified in v2.1.1)

Previously in `core/agent.md` `<team>` section. Removed because all subagents now default to inherit (system default). Kept here for reference.

```
**Model selection:** Every Task dispatch has an optional `model` parameter:
- **`model: "fast"`** — lighter, faster, significantly cheaper. **Use as default for most tasks.** Sufficient for well-scoped work: commands, single-file edits, checklist verification, targeted fixes, routine implementation.
- **Omit `model` (inherit)** — stronger reasoning, slower, costlier. Use when: (a) a task failed with fast — retry with inherit, or (b) a core module that directly determines output quality and requires deep reasoning. Break large core modules into smaller pieces first; only use inherit on the parts that truly need it.

**Full mode:** If the user explicitly requests full mode, shift the balance — use inherit for all quality-sensitive work (core implementation, QA, report writing, complex debugging). Still use fast for simple tasks (file reads, config, commands, lightweight verification).

Example — fast: `Task(subagent_type="executor", model="fast", prompt="...")`
Example — inherit: `Task(subagent_type="executor", prompt="...")`

Role defaults (standard mode):

| Role | Default | Use inherit when |
|------|---------|-----------------|
| executor | fast | core module affecting output quality, or failed with fast |
| report-writer | default | — (always inherit: writes content + formats) |
| QA Specialist | fast | core module or final review → inherit |
| Verifier | fast | core module or final review → inherit |
| Debugger | fast | complex multi-file fix |
| file-extractor | fast | — |
| explore (built-in) | fast | — |
| shell (built-in) | fast | — |
```
