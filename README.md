# General Coding Agent

A multi-agent orchestration system for [Cursor IDE](https://cursor.com/). The **Orchestrator** (tech lead) plans, decomposes tasks into modules, delegates to specialized **subagents**, and drives quality through a structured review pipeline.

## Architecture

```
Orchestrator (agent.md)
├── executor        — General-purpose implementation: code, commands, tests, setup
├── report-writer   — Report writing and formatting: PDF, HTML, slides
├── verifier        — Exhaustive code reviewer at senior-engineer bar (fixes minor, reports major, proposes enhancements)
├── qa-specialist   — Exhaustive black-box output inspector at senior-engineer bar (proposes enhancements; Full / Format / Lightweight modes)
├── debugger        — Targeted fixes from issue lists (scoped to allowed files)
├── file-extractor  — Document & web page extraction (PDF, DOCX, PPTX, URLs)
├── explore         — (built-in) Codebase navigation and keyword search
├── bash            — (built-in) Standalone command execution
└── browser         — (built-in) Browser automation and web app testing
```

## Workflow

```
1. Initialize           — Set up workspace (brief.md + index.md), extract documents / explore codebase when needed, resolve blockers
2. Plan                 — Decompose into modules with dependency graph, define pipelines
3. Module execution     — Per-module Execute -> Check -> Fix -> Reflect loop with mandatory qa-specialist for user-facing output
4. Final content review — Verifier (code) + qa-specialist (Full, content) with enhancement loop (mandatory gate)
5. Report               — Report-writer produces the final deliverable (if formatting is needed)
6. Format QA            — qa-specialist (Format mode) on the rendered deliverable (skipped if step 5 was skipped)
7. Deliver              — Summary to user (open issues, deviations, declined enhancements explicit)
```

### Tiered Quality Control

Every module runs an Execute -> Check -> Fix -> Reflect loop (max 3 rounds):

| Module type | Mid-module QC | When to use |
|-------------|---------------|-------------|
| **Produces user-facing output** (figures, data, text, any deliverable artifact) | `qa-specialist` (Full) at module close — non-negotiable | Anything the user will see or that feeds a later deliverable |
| **Core code module** (complex logic or architecture) | `verifier` for code review | Modules that directly determine correctness or architecture |
| **Internal infrastructure only** (setup, scaffolding, pure library) | Orchestrator self-review | Modules with no user-facing output |

Final content review (`verifier` + `qa-specialist` Full) with an **enhancement loop** is mandatory before any formatting work. After `report-writer` produces the deliverable, a dedicated Format QA pass (`qa-specialist` Format mode) checks rendering, typography, and layout.

## Model Selection

| Mode | Behavior |
|------|----------|
| **Default** | `composer-2` for most work (executor implementation, debugger, file-extractor, routine bash / explore); inherit only for quality-critical judgment (final `verifier`, final `qa-specialist`, `report-writer` primary deliverable, core algorithm design) |
| **Full mode** | inherit for all subagents — no `composer-2` |

## Repository Structure

```
general-coding-agent/
├── core/                          # Agent definitions (source of truth)
│   ├── agent.md                   #   Orchestrator (-> ~/.cursor/commands/)
│   └── subagents/                 #   Subagent definitions (-> ~/.cursor/agents/)
├── skills/                        # Skills referenced by subagents (-> ~/.cursor/skills/)
│   ├── file-content-extraction/   #   PDF/DOCX/PPTX extraction
│   ├── webpage-content-extraction/#   Web page extraction
│   ├── report-builder/            #   Build scripts, LaTeX templates, HTML styles
│   └── pptx/                      #   Slide creation/editing
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
- `skills/*/` -> `~/.cursor/skills/`

## Usage

In Cursor, invoke the orchestrator with `/agent` followed by your task. Provide input files and specify the output directory.

The orchestrator creates a `.workspace/` directory inside the output dir as persistent working memory:

- `brief.md` — frozen task brief (original task, hard constraints, deliverable definition). Never edited after initialization.
- `plan.md` — running plan with per-module sections, updated at every reflect gate (progress, new thinking, problem log, plan adjustments).
- `index.md` — document registry and per-module progress ledger (primary "where am I" source after context compaction).
- `documents/module<N>/` — subagent reports for each module (executor, verifier, qa, debugger).
- `documents/final/` — reports from the final content review and Format QA gates.

Task outputs live alongside `.workspace/` in canonical folders — created only as needed, nothing else allowed at the top level:

`inputs/`, `src/`, `data/`, `outputs/` (runtime artifacts), `deliverables/` (the single authoritative endpoint), `save/` (archive for superseded versions).

If the orchestrator reports that a required file is missing, it will create `.workspace/uploads/` for that task and ask you to place the missing files there.

For development and iteration workflows, see `llm.md`.
