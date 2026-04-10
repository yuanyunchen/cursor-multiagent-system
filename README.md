# General Coding Agent

A multi-agent orchestration system for [Cursor IDE](https://cursor.com/). The **Orchestrator** (tech lead) plans, decomposes tasks into modules, delegates to specialized **subagents**, and drives quality through a structured review pipeline.

## Architecture

```
Orchestrator (agent.md)
├── executor        — General-purpose implementation: code, commands, tests, setup
├── report-writer   — Report writing and formatting: PDF, HTML, slides
├── verifier        — Comprehensive code reviewer (fixes minor, reports major)
├── qa-specialist   — Black-box output inspector (Full / Lightweight modes)
├── debugger        — Targeted fixes from issue lists (scoped to allowed files)
├── file-extractor  — Document & web page extraction (PDF, DOCX, PPTX, URLs)
├── explore         — (built-in) Codebase navigation and keyword search
├── bash            — (built-in) Standalone command execution
└── browser         — (built-in) Browser automation and web app testing
```

## Workflow

```
1. Initialize    — Set up workspace, extract documents when needed, explore codebase when needed, create `uploads/` only for missing user files
2. Plan          — Decompose into modules, define pipelines
3. Execute       — Per-module execution with tiered quality control
4. Final Review  — Verifier + QA on all deliverables (mandatory gate)
5. Report        — Report-writer produces final documents (if needed)
6. Deliver       — Summary to user
```

### Tiered Quality Control

Modules are classified as **routine** or **core** at planning time:

| Module Type | Pipeline | When to Use |
|-------------|----------|-------------|
| **Routine** | executor -> orchestrator check | Straightforward implementation that is quick to validate directly |
| **Core**    | executor -> orchestrator check (+ verifier / qa-specialist as needed) | Modules that directly determine output quality or need deeper review |

Final review (verifier + QA) is mandatory before every delivery.

## Model Selection

| Mode | Behavior |
|------|----------|
| **Default** | inherit for quality-critical work (core modules, verifier, QA, report-writer); fast for routine tasks |
| **Full mode** | inherit for all subagents |

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

If the orchestrator reports that a required file is missing, it will create `.workspace/uploads/` for that task and ask you to place the missing files there.

For development and iteration workflows, see `llm.md`.
