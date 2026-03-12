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
| file-explorer | `file-explorer.md` | Document extraction and organization. Two-phase: extract (via file-content-extraction skill) then organize (restructure, integrate figures, remove noise). Handles PDF, DOCX, PPTX. |

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
