# Version History

## v2.6.1 (2026-04-27)

Prompt density pass on `core/agent.md` and `llm.md`; report-prompt optimization for `report-writer` + `write-report` skill (per `iterations/current/requirements/report-prompt-optimization.md`); expanded snapshot scope for `deploy.sh --archive`.

### Changes

- **`core/agent.md` density pass (390 → 271 lines).** Folded `<team>` I/O field listings (covered by `<task_format>`); removed the trailing per-agent field bullet list under `<task_format>`; replaced workflow Step 3's "step 0 Re-ground" sub-block with a Rule 7 reference; collapsed Step 5 producer-specific bullets that restated `<team>`; replaced the standalone "producer evidence cleanup" paragraph with a Rule 8 reference; trimmed Rule 1 / Rule 5 / Rule 6 / Rule 8 sub-bullets that duplicated `<role>`, `<task_format>`, `<workspace>`, and workflow content. All features, dispatch modes, conditional paths, and rule sub-bullets preserved.
- **`llm.md` density pass (290 → 144 lines).** Removed the `Core File Roles` table (each subagent / skill owns its own description as the single source of truth); merged the cross-file consistency checklist that lived in both Principle 2 and Phase 2; folded the `Versioning` commit-protocol with Phase 5; pruned tone-only sentences.
- **Versioned snapshot scope expanded.** `scripts/deploy.sh --archive` now writes `core/`, `skills/`, and `scripts/` snapshots to `iterations/current/files/{core,skills,scripts}/` (previously only `core/`). `llm.md` documents the new layout under "Iterations" and Phase 3.
- **Report prompt optimization.** `core/subagents/report-writer.md` (266 → ~135 lines) and `skills/write-report/SKILL.md` (~200 → ~135 lines) rewritten per the boundary defined in `iterations/current/requirements/report-prompt-optimization.md`: skill owns format/tooling layer, `report-writer.md` owns content/orchestration layer; no overlapping content.

### Files Modified

- `core/agent.md`
- `core/subagents/report-writer.md`
- `llm.md`
- `scripts/deploy.sh`
- `skills/write-report/SKILL.md`
- `history.md` (v2.6 back-fill + v2.6.1 entry)

### Tested On

- Cross-file consistency: subagent YAML descriptions still align with `<team>` rows; XML tag set unchanged; rule cross-references (Rule 4 / 7 / 8) still valid.
- `deploy.sh` dry-run via actual deploy (1 command + 7 subagents + 8 skills synced).

## v2.6 (2026-04-27)

Redesign of report production workflow.

### Changes

- **Replace `report-builder` with `write-report` skill** and local LaTeX starters (templates moved into the project).
- **Clarify `report-writer` ownership**, context feedback (`NEEDS_MORE_CONTEXT` handshake), and QA cleanup contract.
- **Route HTML reports and web deliverables through `frontend-engineer`** (report-writer scope tightened to LaTeX PDF only).
- **Soften report and QA structures into flexible reference formats** rather than fixed schemas.

### Files Modified

- `README.md`, `core/agent.md`, `core/subagents/qa-specialist.md`, `core/subagents/report-writer.md`, `llm.md`, `scripts/deploy.sh`, `skills/write-report/` (new skill replacing `skills/report-builder/`)

(Back-filled retroactively in v2.6.1 — the v2.6 commit itself did not include a `history.md` entry.)

## v2.5 (2026-04-24)

New `frontend-engineer` subagent; workflow integration of design + build + test for web frontends; removal of standalone Format QA step.

### Changes

- **New subagent `frontend-engineer`.** Owns the entire web-frontend deliverable in one role: design direction (via `frontend-design` + `theme-factory`), build (static HTML/CSS or React via `web-artifacts-builder`), and an internal iterative render-inspect-fix QA loop (via `webapp-testing` / Playwright). Two modes — **Full** (design + build + test) and **Polish** (improve / debug / test-only on an existing artifact). Writes `frontend_qa.md` (mirrors `qa-specialist`'s coverage / blockers / enhancement sections) and iterates up to 4 rounds. Two equally weighted quality axes — design intentionality and the QA loop.
- **`frontend-engineer` is dual-use.** Can serve as a Step 3 module executor for any frontend module *or* as the Step 5 final producer when the entire deliverable is a frontend. Step 5 collapses into a confirmation when frontend was already built in Step 3.
- **Workflow Step 6 (Format QA) removed.** `report-writer` and `frontend-engineer` each run their own internal iterative QA loop and write a producer QA report (`report_qa.md` / `frontend_qa.md`), so a separate global format-QA pass is no longer in the workflow. New numbered steps: 1) Initialize, 2) Plan, 3) Module execution, 4) Final content review, 5) Final deliverable production, 6) Deliver.
- **Step 4 wording — "before final deliverable production".** Replaces "before any formatting work". Step 4 also gains a **Skip-or-collapse condition**: when the entire deliverable is a frontend produced by `frontend-engineer`, dispatch `verifier` only on non-frontend code and skip `qa-specialist` Full at this gate (its job is fully covered by `frontend_qa.md`).
- **Module-close QA — internal-QA exception.** When a module is implemented by `frontend-engineer` or `report-writer`, their internal QA report satisfies module-close QA; the orchestrator confirms PASS verdict from the producer's report and does **not** dispatch a redundant `qa-specialist` Full pass. Multi-system integration QA still runs.
- **Producer 4-round fallback.** When a producer hits its 4-round cap with blockers remaining, the orchestrator may dispatch `debugger` for at most one fix round, then `resume` the producer for one final render-inspect cycle. If blockers persist, stop and escalate to the user with a best-effort delivery plus a "Known open issues" enumeration.
- **`frontend-engineer` always uses `<output><output_dir>`.** Frontend projects are inherently multi-file (source + built artifact + assets), so the I/O contract is single-tagged for clarity. `<task_format>` notes and the `<workspace>` Naming Conventions table updated accordingly.
- **`browser` built-in scope clarified.** Reserved for orchestrator ad-hoc browser automation (one-off navigation, quick screenshot, blocker diagnosis). Full frontend test loops and design-build-test work go to `frontend-engineer`.
- **Frontend skills brought into the project.** `skills/frontend-design/`, `skills/theme-factory/`, `skills/web-artifacts-builder/`, `skills/webapp-testing/` are now tracked alongside the existing `file-content-extraction`, `webpage-content-extraction`, `report-builder`, and `pptx` skills. `deploy.sh` already iterates over `skills/*/`, so no script change was needed; the project is now self-contained for fresh deployments.
- **`report-writer` scope tightened.** Stays the report producer (PDF, slides). HTML is used only as a PDF source (`pdf-html`); standalone webpages are delegated to `frontend-engineer`. Internal QA loop now writes `report_qa.md` (parallel to `frontend_qa.md`) — same exception applies for module-close QA.
- **Documentation alignment.** `README.md`, `llm.md`, and `core/agent.md` `<team>` table all reflect the new subagent, the dual-use dispatch model, the internal-QA exception, and the removed Format QA step.

### Files Modified

- `core/agent.md` — `<team>` table (added `frontend-engineer` row, updated `report-writer` row, clarified `browser` scope), `<workflow>` Step 3 Execute (dispatch model), Step 3 Check (internal-QA exception), Step 4 (rewording + skip-or-collapse), Step 5 (collapse + 4+1 fallback), removed Step 6 Format QA, `<task_format>` (frontend-engineer uses `output_dir`), Naming Conventions table
- `core/subagents/frontend-engineer.md` — new file
- `core/subagents/report-writer.md` — YAML description, role intro, internal QA loop section, `report_qa.md` format, rules (HTML-as-PDF-source only, standalone webpage delegation)
- `README.md` — architecture (added `frontend-engineer`, clarified `browser`), workflow (6 steps), tiered QC table, model selection, repository structure (added 4 frontend skills)
- `llm.md` — workspace tree (added 4 frontend skills), Core File Roles (added `frontend-engineer.md` + 4 skill rows)
- `skills/frontend-design/`, `skills/theme-factory/`, `skills/web-artifacts-builder/`, `skills/webapp-testing/` — new (copied from `~/.cursor/skills/`)
- `history.md` — v2.5 entry

### Tested On

- Manual cross-file consistency review (`agent.md`, `frontend-engineer.md`, `report-writer.md`, `README.md`, `llm.md`) — workflow numbering, dispatch model, I/O contract, Step 6 removal
- IDE lint check on modified markdown files (no linter errors)
- `deploy.sh` dry-run via actual deploy: 1 command + 7 subagents + 8 skills synced, including the 4 newly-tracked frontend skills

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

## v2.3.1 (2026-04-10)

Prompt contract cleanup, consistency alignment, and orchestrator attention tuning.

### Changes

- **Unified dispatch contract clarified.** `core/agent.md` now uses a structured `<output>` schema (`report`, `standards`, `deliverable`, `output_dir`) and all subagent prompts were updated to consume the same fields.
- **Cross-file consistency tightened.** Synced built-in names, report-writer capabilities, README workflow wording, and `llm.md` consistency checks so public docs and runtime prompts describe the same behavior.
- **Workspace upload flow formalized.** Added explicit `.workspace/uploads/` behavior for blocker-driven user file uploads, with creation only when missing user-provided materials block execution.
- **Prompt quality improved without changing behavior.** Simplified orchestrator wording, replaced the domain-biased planning example with a more general one, and front-loaded operational priorities plus blocker handling.

### Files Modified

- `core/agent.md`
- `core/subagents/executor.md`
- `core/subagents/verifier.md`
- `core/subagents/debugger.md`
- `core/subagents/qa-specialist.md`
- `core/subagents/file-extractor.md`
- `core/subagents/report-writer.md`
- `llm.md`
- `README.md`

### Tested On

- Manual consistency review across `agent.md`, subagent prompts, `llm.md`, and `README.md`
- IDE lint check on modified markdown files (no linter errors)

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

## v2.2 (2026-04-03)

Document subagent task parameters and session control.

### Changes

- **Added a dedicated `<parameters>` section to `core/agent.md`.** Separated task-call parameter guidance from the team table for clearer usage documentation.
- **Documented background agent behavior.** Added guidance for `run_in_background`, transcript monitoring, and the fact that completion is not pushed automatically.
- **Documented resume-based session continuation.** Added `resume` guidance for continuing the same foreground or background agent session instead of starting a new one.
- **Added minimal call examples.** Included compact examples for normal dispatch, background dispatch, and resume calls.

### Files Modified

- `core/agent.md` — added `<parameters>` section with model selection, background agent, resume session, and call examples
- `history.md` — added v2.2 entry

## v2.1.2 (2026-03-14)

Versioning scheme and commit protocol.

### Changes

- **Versioning scheme defined.** `major.minor.patch` — major for architecture, minor for features (user-assigned), patch auto-increments per commit.
- **Commit protocol formalized.** Every commit: deploy -> append `history.md` entry -> commit -> report (old version -> new version + changes).
- **Retroactive patch version.** Added v2.1.1 entry for the previous unversioned commit.

### Files Modified

- `llm.md` — new "Versioning" section with scheme + commit protocol
- `history.md` — v2.1.1 and v2.1.2 entries added

## v2.4.3 (2026-04-17)

Project renamed to **Cursor Multiagent System**.

### Changes

- **GitHub repo renamed** from `general-coding-agent` to `cursor-multiagent-system`. Remote URL auto-updated on local clone.
- **Local directory renamed** from `general-coding-agent/` to `cursor-multiagent-system/`.
- **`README.md` title** updated to "Cursor Multiagent System"; repository-structure tree root updated accordingly.
- **`llm.md`** — opening line and all path examples (`Workspace Structure` tree, `prompt.txt` format, naming conventions) updated to use the new name.

### Files Modified

- `README.md`
- `llm.md`
- `history.md`

## v2.4.2 (2026-04-17)

Single-branch (main-only) policy.

### Changes

- **Merged `v2.3-quality-overhaul` into `main`** (fast-forward, all commits preserved); feature branch deleted locally and on origin. Going forward, `main` is the only working branch.
- **Branch protection adjusted.** `enforce_admins` disabled so the repo owner can push directly to `main`. Review requirement kept for external contributors; force-push and branch deletion on `main` remain blocked.
- **`llm.md` — new "Git Branch Policy" section.** Documents the main-only policy, admin direct-push, PR-required-for-externals, feature-branches-only-for-high-risk-work. Commit protocol step list updated to state "push directly to `main`" explicitly.

### Files Modified

- `llm.md`
- `history.md`

## v2.4.1 (2026-04-17)

README alignment with v2.4 logic.

### Changes

- **qa-specialist architecture line** brought in line with verifier: "Exhaustive black-box output inspector at senior-engineer bar (proposes enhancements; Full / Format / Lightweight modes)".
- **Workflow Step 5-6 conditionality clarified.** Report step marked as "if formatting is needed"; Format QA step noted to be skipped when Report is skipped.
- **Usage section extended with workspace state files.** Added explicit descriptions of `brief.md`, `plan.md`, `index.md`, `documents/moduleN/`, `documents/final/`, plus the 5+1 canonical task-output folders (`inputs/`, `src/`, `data/`, `outputs/`, `deliverables/`, `save/`) so end users understand what the orchestrator creates inside the output dir.

### Files Modified

- `README.md`
- `history.md`

## v2.4 (2026-04-17)

Dispatch control, workspace contract, and quality-bar overhaul.

### Changes

- **Dispatch mode — foreground-batched default, background for independent long tasks.** Rewrote `<parameters>` to prescribe: group independent subagents into a single foreground parallel batch by default; use `run_in_background` only when (a) the task is noticeably longer than the current bottleneck and (b) the orchestrator has real work to do alongside. `Await` is used once at the bottleneck — continuous polling is prohibited. Same rule applies to long-running shell commands.
- **Module dependency graph in plans.** Planning now requires an explicit dependency graph after module specs so the orchestrator can schedule parallel branches vs. bottleneck chains.
- **Model selection rebalanced.** `composer-2` is now the default for most work (executor implementation, debugger, file-extractor, routine explore / bash). Inherit is reserved for quality-critical judgment: final `verifier`, final `qa-specialist`, `report-writer` primary deliverable, and core algorithm design. Plan example updated to match.
- **Externalized orchestrator memory.** Formalized three canonical workspace files:
  - `brief.md` — frozen task brief (original task, constraints, deliverable definition, dispatch-norms reminder, task-output layout map). Never edited after initialize.
  - `index.md` — directory tree, document registry, per-module progress ledger (dispatched → returned → verdict → key paths), open decisions.
  - `plan.md` — running plan with per-module headings updated at every reflect gate (progress, new thinking, problems, plan adjustments with rationale).
- **Workspace contract — 5+1 canonical task-output folders.** `inputs/`, `src/`, `data/`, `outputs/`, `deliverables/`, `save/` — created on demand, nothing else allowed at top level. `deliverables/` is the single authoritative endpoint (copy-not-link). Document reports live under `documents/moduleN/` with role-based filenames; superseded reports go to `documents/save/`. Naming conventions made mandatory with deviation requiring a one-line note in `index.md`.
- **Rule 7 — Orchestrator memory is untrusted.** New rule mandating targeted re-reads at decision points: the current module's section of `plan.md`, the previous module's ledger line, and — when dispatch protocol is uncertain — the specific rule / `<parameters>` / `<task_format>` block in the deployed system prompt, not the whole file. Recovery checkpoint: when orchestrator cannot clearly recall brief / last module / current step, stop and re-read.
- **Rule 8 — Workspace hygiene.** New rule enforcing agile, non-accumulative workspace: archive superseded artifacts to `documents/save/` or `save/` in the same turn the replacement is committed; delete clearly-trash files outright; no dead code, no duplicates, no drift; single authoritative location per concept; pre-delivery cleanup sweep is a quality gate, not a polish step.
- **Mid-module QA mandatory for user-facing output.** Module Check step now requires `qa-specialist` (Full) at module close for any module producing user-facing output (figures, data files, text, any deliverable artifact). Final QA cannot exhaustively inspect hundreds of accumulated artifacts, and deferring loses the ability to resume the producing subagent for fixes.
- **Final review split: content vs. format.** Replaced the single Final Review step with three distinct steps:
  - Step 4 **Final content review** — `verifier` + `qa-specialist` Full (in parallel), with a pre-review cleanup pass and an **Enhancement loop** (pursue HIGH/MEDIUM suggestions by default; decline only with explicit rationale in `plan.md`).
  - Step 5 **Report** — `report-writer` runs only after content is locked.
  - Step 6 **Format QA** — `qa-specialist` Format mode for rendering/layout only; no content re-audit.
- **QA Specialist — Format mode added, Full mode raised.** Three modes now: Full (content QA), Format (rendering/layout, no content re-audit), Lightweight. Full mode workflow requires exhaustive inspection (every visual artifact via `Read`, every page), senior-engineer bar, and substantive enhancement analysis as a first-class section.
- **Verifier — senior-engineer bar, exhaustive, enhancement analysis required.** Reviews every file in scope holistically, not just against checklist. Enhancement analysis is a required first-class section ranked by impact (HIGH / MEDIUM / LOW) with domain-specific guidance (ML: hyperparameter search, ablations; systems: failure modes, concurrency; etc.).
- **Rule 4 — Quality-first mindset.** Passing QA means "no blockers AND no unaddressed reasonable enhancements", not "no blockers". Act on HIGH/MEDIUM suggestions by default; decline only with explicit rationale in `plan.md`.
- **Rule 2 — Blockers: stop immediately, escalate in the user's language.** Expanded blocker categories to explicitly cover runtime environment gaps (GPU/CUDA, OS-specific tools, missing network), credentials (API keys, HuggingFace / OpenAI tokens), and missing inputs requiring download. The orchestrator halts at discovery and states what is blocked, why, and what the user must provide — no silent fallbacks.
- **Summary format — explicit transparency.** Reply in the user's prompt language. Replaced vague "Honest assessment" with mandatory bulleted sections: Known open issues (every unresolved issue from verifier / qa-specialist reports with location and reason), Deviations from requirements, Declined enhancements (with rationale from `plan.md`), Suggested next steps. Hiding issues is a delivery-step failure.

### Files Modified

- `core/agent.md` — dispatch `<parameters>`, workflow (re-ground step, mid-module QA, split final review, format QA), rules (Rule 2 blockers, Rule 4 quality-first, Rule 6 directory ownership, Rule 7 untrusted memory, Rule 8 hygiene), `<workspace>` (brief/index/plan roles, 5+1 folder contract, module subfolders, mandatory naming), summary format
- `core/subagents/qa-specialist.md` — YAML description, added Format mode, Full mode workflow (exhaustive + enhancement analysis), rules (senior-engineer bar, exhaustive not sampled, enhancement analysis required)
- `core/subagents/verifier.md` — YAML description, workflow (exhaustive review + enhancement analysis), output format (Enhancement Analysis first-class section), rules (senior-engineer bar, exhaustive not sampled, enhancement analysis required)
- `README.md` — architecture note for verifier/qa-specialist Format mode, workflow (7 steps), tiered QC table (mandatory mid-module QA), model selection (composer-2 default)
- `history.md` — v2.4 entry

### Tested On

- Manual consistency review across `agent.md`, subagent prompts, `README.md`, and `llm.md` checklist
- IDE lint check on modified markdown files (no linter errors)

## v2.3 (2026-04-10)

Input validation, escalation protocol, and quality control overhaul.

### Changes

- **Initialize step expanded (4 phases).** Added Validate Inputs (check all referenced files exist and extracted successfully), Clarify Requirements (identify blockers, ambiguities, technical choices), and User Confirmation Gate (structured summary with blockers/questions, must resolve before planning). Previously Initialize only had workspace setup and requirement aggregation.
- **Escalation protocol (Rule 7).** New rule: stop and ask the user when encountering blockers (missing files, conflicting requirements, extraction failures, infeasible constraints). Overrides bias toward producing output — delivering nothing beats silently deviating from requirements.
- **Unified module execution loop.** Replaced separate routine/core module flows with a single Execute → Check → Fix → Reflect loop. Check intensity based on result complexity (simple: self-review, complex: qa-specialist), not module type.
- **Module Check criteria in plans.** Each module now defines a **Check** field specifying what to verify after execution — key outputs, metrics, what "correct" looks like.
- **Orchestrator quality ownership.** Role updated: orchestrator is the final owner of output quality, reviews key outputs (data, metrics, intermediate results) at check and reflect gates.
- **Verifier scoped to core + final review.** Removed verifier from the default module loop. Now dispatched only for core modules with complex logic and Step 4 (Final review).
- **Executor flag-blockers rule.** New Rule 9: stop and report when referenced files/resources don't exist or requirements are unrealistic — no guessing, no synthetic substitutes, no silent skips.

### Files Modified

- `core/agent.md` — role, workflow (Initialize expanded, module execution unified, plan Check field), rules (Rule 1 quality oversight, Rule 3 intermediate results, Rule 7 escalation), team table (verifier, debugger descriptions)
- `core/subagents/executor.md` — Rule 9 (flag blockers)
- `core/subagents/verifier.md` — YAML description updated (core modules and final review only)
- `history.md` — v2.3 entry

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
