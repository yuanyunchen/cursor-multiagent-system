# Version History

## v1.0 (2026-03-10)

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

---

## v1.1 (2026-03-11)

Added workspace filesystem, planning/reflection workflow, cost-aware model selection, orchestrator direct execution, and task merging. Systematized the development process in `llm.md`.

### Workspace Filesystem (`<workspace>` section in `agent.md`)

- `.workspace/` directory created for M/L tasks inside output directory.
- Structured files: `index.md`, `analysis/understanding.md`, `analysis/standards.md`, `plan/plan_v0.md`, `plan/plan.md`, `history/execution_log.md`, `dispatches/T-{N}_context.md`, `dispatches/T-{N}_output.md`, `content/`.
- Orchestrator manages workspace; subagents write only to their designated output files.
- File-based context transfer replaces inline context for M/L tasks, saving tokens and creating audit trails.

### Planning and Reflection Workflow (workflow restructure in `agent.md`)

- M tasks: Analyze -> Plan -> Execute (with reflect gates every 2-3 rounds) -> Validate -> Iterate -> Deliver.
- L tasks: Understand -> Analyze -> Architect/Plan -> Execute (with mandatory reflect gate every round + checkpoint validation) -> Final Validate -> Iterate -> Deliver.
- Mandatory Analyze phase writes `understanding.md` and `standards.md` before execution.
- Mandatory Plan phase produces frozen `plan_v0.md` and living `plan.md`.
- Reflect gates compare progress against plan, update living plan, and append to execution log.

### Cost-Aware Model Selection (Rules 1, 7; `<team>` model selection in `agent.md`)

- Explicit model IDs: `kimi-k2.5`, `gpt-5.4`, `claude-4.6-opus`, `gpt-5.4-high`, `claude-4.6-opus-high-thinking`.
- Tiered system: Standard (`kimi-k2.5`), High (`gpt-5.4`, `claude-4.6-opus`), High+ (Full mode only).
- User specifies Standard or Full mode at task start.
- Model switching on failure: retry with different model at same or higher tier.
- QA/Verifier model rotation across QC rounds for multi-perspective review.

### Orchestrator Direct Execution (Rule 1 in `agent.md`)

- Orchestrator executes small tasks directly (reading <=2 files, editing <=1 file, <=3 tool calls) when delegation overhead exceeds task value.
- All `.workspace/` file writes are always done directly by orchestrator.

### Task Merging (Rule 3 in `agent.md`)

- Related small tasks sharing context merged into single subagent dispatch.
- Each subagent dispatch's value must justify its fixed overhead.

### Subagent Updates

- executor, designer: Added Task Input and Workspace Integration sections for file-based dispatch.
- qa-specialist, verifier: Added Task Input sections referencing `standards.md`.
- debugger: Updated Task Input section for file-based context.
- file-explorer: Added workspace integration for saving to `.workspace/content/` and updating `index.md`.

### Development Process (`llm.md`)

- Added Agent Design Principles section (description balance, cross-file consistency, surgical edits, compatibility, requirements-first).
- Added `requirements/` directory to iteration workspace structure.
- Replaced Version Update Checklist with 5-phase Version Transition procedure.
- Updated Core File Roles table.
- Documented iteration artifacts: requirements, problems.md, code_review.md, human_feedback.md.

### Files Modified

- `core/agent.md` (major: new `<workspace>`, rewritten rules 1-3/7, new rule 8, restructured workflow, updated `<team>`, `<task_format>`, `<iteration_control>`, `<summary_format>`)
- `core/subagents/executor.md`, `designer.md`, `qa-specialist.md`, `verifier.md`, `debugger.md`, `file-explorer.md` (minor: workspace integration sections)
- `llm.md` (updated: design principles, workspace structure, version transition procedure)

---

## v1.2 (2026-03-11)

Major simplification and refinement of the orchestration system based on test runs.

### Model Selection Simplification
- Reduced from 5 explicit model IDs + 3 tiers to `fast` vs `inherit` (Cursor Task tool limitation).

### Workspace Overhaul
- Removed `dispatches/` (context/output files). Communication uses default Cursor mechanism.
- Added `documents/` for reusable artifacts (write once, reference by path).
- Removed `understanding.md`. Replaced `analysis/` with `standards/` (per-module files).
- `execution_log.md` written once at end, not per-step.

### Quality Pipeline
- Reordered: Implementation → Verifier → Debug → QA → Designer.
- QA before Designer (content verified before formatting). No QA after designer.
- Verifier can fix obvious issues directly. All QC agents do holistic review beyond standards.
- Execute ↔ Verify ↔ QA loop with three gate levels per sub-module.

### Workflow Changes
- Removed user confirmation for plans. Autonomous execution by default.
- Plans define dispatch strategy (agent type + model, parallel groups, quality checkpoints with feedback loops). Not 1:1 task-to-agent.
- Scope isolation: Input files only, no browsing other results.
- Output containment: all files in Output directory, clean up before delivery.
- Delegation autonomy: goals and constraints, not step-by-step instructions.
- Honest assessment in delivery summary.

### Other
- Designer may trim/rephrase for layout conventions (preserving meaning).
- Deploy script `--archive` flag. Logging format uses agent-type (model) not T-N numbering.
- `llm.md`: default auto-commit, current-first versioning workflow.

### Files Modified
- `core/agent.md` (major: simplified model selection, workspace overhaul, quality pipeline reorder, execute-verify-QA loop, new rules 7-8-10, workflow restructure, delegation autonomy, honest summary)
- `core/subagents/verifier.md` (major: can fix issues, holistic scan, new output format)
- `core/subagents/qa-specialist.md` (holistic review, standards as starting point)
- `core/subagents/designer.md` (may trim/rephrase content)
- `core/subagents/executor.md` (output containment rule)
- `core/subagents/debugger.md` (updated trigger description)
- `llm.md` (auto-commit, deploy --archive, current-first versioning)
- `scripts/deploy.sh` (--archive flag)
