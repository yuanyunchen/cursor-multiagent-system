# Cursor Multiagent System

A multi-agent orchestration system for [Cursor IDE](https://cursor.com/). The **Orchestrator** (tech lead) plans, decomposes tasks into modules, delegates to specialized **subagents**, and drives quality through a structured review pipeline.

## Architecture

```
Orchestrator (agent.md)
├── executor          — General-purpose implementation: code, commands, tests, setup
├── report-writer     — Professional LaTeX PDF reports only. Owns content + LaTeX formatting, uses write-report templates, requests missing context when needed, writes report_qa.md.
├── frontend-engineer — HTML reports/posters, static pages, dashboards, and interactive web deliverables. Design, build, optimize, test. Standard render/test-inspect-fix-cleanup QA loop, writes frontend_qa.md.
├── verifier          — Exhaustive code reviewer at senior-engineer bar (fixes minor, reports major, proposes enhancements)
├── qa-specialist     — Exhaustive black-box output inspector at senior-engineer bar (proposes enhancements; Full / Format / Lightweight modes)
├── debugger          — Targeted fixes from issue lists (scoped to allowed files)
├── file-extractor    — Document & web page extraction (PDF, DOCX, PPTX, URLs)
├── explore           — (built-in) Codebase navigation and keyword search
├── bash              — (built-in) Standalone command execution
└── browser           — (built-in) Ad-hoc browser automation (quick checks; for full frontend test loops, dispatch frontend-engineer)
```

## Workflow

```
1. Initialize                       — Set up workspace (brief.md + index.md), extract documents / explore codebase when needed, resolve blockers
2. Plan                             — Decompose into modules with dependency graph, define pipelines
3. Module execution                 — Per-module Execute -> Check -> Fix -> Reflect loop with mandatory qa-specialist for user-facing output; multi-system integration modules also get end-to-end qa-specialist Full
4. Final content review             — Verifier (code) + qa-specialist (Full, content) with enhancement loop (mandatory gate)
5. Final deliverable production     — report-writer (LaTeX PDF reports) or frontend-engineer (HTML reports/posters/static pages/dynamic web apps) produces the final deliverable, running its own internal iterative QA loop (max 4 rounds)
6. Deliver                          — Summary to user (open issues, deviations, declined enhancements explicit)
```

### Tiered Quality Control

Every module runs an Execute -> Check -> Fix -> Reflect loop (max 3 rounds):

| Module type | Mid-module QC | When to use |
|-------------|---------------|-------------|
| **Produces user-facing output** (figures, data, text, any deliverable artifact) | `qa-specialist` (Full) at module close — non-negotiable | Anything the user will see or that feeds a later deliverable |
| **Multi-system integration** (frontend + backend, multi-service) | `qa-specialist` (Full) at module close for end-to-end integration QA | Even when individual components were already QA'd in their own modules |
| **Core code module** (complex logic or architecture) | `verifier` for code review | Modules that directly determine correctness or architecture |
| **Internal infrastructure only** (setup, scaffolding, pure library) | Orchestrator self-review | Modules with no user-facing output |

Final content review (`verifier` + `qa-specialist` Full) with an **enhancement loop** is mandatory before final deliverable production. The producers (`report-writer` for LaTeX PDF reports, `frontend-engineer` for HTML reports/posters/static pages/dynamic web apps) each run their own standard iterative QA loop (render/test -> inspect -> fix -> re-verify -> cleanup, max 4 rounds, each writing its own QA report — `report_qa.md` or `frontend_qa.md`), so a separate global format-QA pass is not part of the workflow. `report-writer` owns report content organization as well as LaTeX formatting; if required results, explanations, figures, or requirements are missing, it returns `NEEDS_MORE_CONTEXT` and the orchestrator resumes the same subagent after preparing the missing material. Loop artifacts such as screenshots, page images, temporary PDF exports, traces, logs, and old builds are not final deliverables; only final-round audit evidence may be retained under `.workspace/documents/module<N>/qa_evidence/final/`.

## Model Selection

| Mode | Behavior |
|------|----------|
| **Default** | `composer-2` for most work (executor implementation, debugger, file-extractor, routine bash / explore); inherit only for quality-critical judgment (final `verifier`, final `qa-specialist`, `report-writer` and `frontend-engineer` on the primary deliverable, core algorithm design, frontend aesthetic direction) |
| **Full mode** | inherit for all subagents — no `composer-2` |

## Repository Structure

```
cursor-multiagent-system/
├── core/                          # Agent definitions (source of truth)
│   ├── agent.md                   #   Orchestrator (-> ~/.cursor/commands/)
│   └── subagents/                 #   Subagent definitions (-> ~/.cursor/agents/)
├── skills/                        # Project-owned skills (-> ~/.cursor/skills/ via deploy.sh)
│   ├── file-content-extraction/   #   PDF/DOCX/PPTX extraction (file-extractor, qa-specialist)
│   ├── webpage-content-extraction/#   Web page extraction (file-extractor)
│   └── write-report/              #   Report writing standards, template cache, build scripts (report-writer)
├── scripts/
│   └── deploy.sh                  #   Deploy core/ and skills/ to Cursor
├── history.md                     # Version history (append-only)
├── llm.md                         # Workspace guide for development iterations
└── README.md
```

## Setup

Deploy agent definitions and skills to Cursor IDE:

```bash
./scripts/deploy.sh
```

This syncs:
- `core/agent.md` -> `~/.cursor/commands/agent.md`
- `core/subagents/*.md` -> `~/.cursor/agents/`
- `skills/*/` -> `~/.cursor/skills/` (project-owned skills only)

### External skill dependencies

Subagents also reference skills the project does **not** vendor — these must be present at `~/.cursor/skills/<name>/SKILL.md` before deploying. Missing skills do not break deployment, but the subagent that needs them will fall back to ad-hoc implementation (defeating the skills-first design).

| Skill | Used by | How to install |
|-------|---------|----------------|
| `pdf` | executor, report-writer | Anthropic Claude skills (symlink from `~/.claude/skills/pdf`) |
| `docx` | executor, qa-specialist | Anthropic Claude skills |
| `xlsx` | executor, qa-specialist | Anthropic Claude skills |
| `pptx` | executor, qa-specialist | Anthropic Claude skills |
| `frontend-design` | frontend-engineer, qa-specialist | Anthropic Claude skills |
| `theme-factory` | frontend-engineer, qa-specialist | Anthropic Claude skills |
| `web-artifacts-builder` | frontend-engineer | Anthropic Claude skills |
| `webapp-testing` | frontend-engineer, qa-specialist, debugger | Anthropic Claude skills |
| `parallel-web-search`, `parallel-deep-research`, `parallel-web-extract`, `parallel-data-enrichment` | executor | Auto-installed by the Parallel Cursor plugin (path is resolved via `Glob` since it contains a commit SHA) |

The Anthropic Claude skills are installed at `~/.claude/skills/` and surfaced via symlinks inside `~/.cursor/skills/`. The project does not pin or vendor these — Anthropic-side updates are picked up automatically.

## Usage

In Cursor, invoke the orchestrator with `/agent` followed by your task. Provide input files and specify the output directory.

The orchestrator creates a `.workspace/` directory inside the output dir as persistent working memory:

- `brief.md` — frozen task brief (original task, hard constraints, deliverable definition). Never edited after initialization.
- `plan.md` — running plan with per-module sections, updated at every reflect gate (progress, new thinking, problem log, plan adjustments).
- `index.md` — document registry and per-module progress ledger (primary "where am I" source after context compaction).
- `documents/module<N>/` — subagent reports for each module (executor, verifier, qa, debugger; plus producer QA reports `report_qa.md` / `frontend_qa.md` for the deliverable production module). Final-round producer evidence, when retained for audit, lives under `qa_evidence/final/`; loop intermediate artifacts are cleaned before delivery.
- `documents/final/` — reports from the final content review gate (`verify.md`, `qa.md`).

Task outputs live alongside `.workspace/` in canonical folders — created only as needed, nothing else allowed at the top level:

`inputs/`, `src/`, `data/`, `outputs/` (runtime artifacts, cleaned before delivery unless explicitly user-facing), `deliverables/` (the single authoritative endpoint), `save/` (archive for superseded versions).

If the orchestrator reports that a required file is missing, it will create `.workspace/uploads/` for that task and ask you to place the missing files there.

For development and iteration workflows, see `llm.md`.
