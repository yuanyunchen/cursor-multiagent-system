# General Coding Agent

A multi-agent orchestration system for Cursor IDE. The **Orchestrator** (tech lead) plans, delegates, and manages quality — while specialized **subagents** handle all hands-on work.

## Architecture

```
Orchestrator (agent.md)
├── executor        — General-purpose implementation: code, commands, tests, setup
├── designer        — Visual deliverables: PDF (LaTeX/HTML), web pages, slides
├── debugger        — Targeted fixes from QA issue lists (scoped to allowed files)
├── qa-specialist   — Read-only output quality inspection (Full / Lightweight modes)
├── verifier        — Fast per-item PASS/FAIL checks against explicit criteria
├── file-explorer   — Document extraction & organization (PDF, DOCX, PPTX)
├── explore         — (built-in) Codebase navigation and keyword search
├── shell           — (built-in) Standalone command execution
└── browser-use     — (built-in) Browser automation and web app testing
```

## Quality Control Loop

The system enforces a closed-loop QC process:

```
QA Specialist (find issues) → Debugger (fix) → Verifier (confirm) → re-QA
                                     ↑                                  |
                                     └──────── max 3 rounds ───────────┘
```

- **QA Specialist** inspects deliverables (never source code) and classifies findings as blockers vs. suggestions
- **Debugger** applies minimal, scoped fixes only to explicitly allowed files
- **Verifier** confirms fixes are correct and in-scope
- Nothing ships without a passed full-mode QA round

## Workflow

| Task Size | Flow |
|-----------|------|
| **S** (single file, <10 lines) | Dispatch one task, scan result, reply |
| **M** (clear scope, few files) | Plan → Execute → Validate → Iterate → Deliver |
| **L** (multi-file, architecture) | Understand → Architect → Execute in rounds (with checkpoints) → Final Validate → Iterate → Deliver |

Key principles:
- **Delegate everything.** The orchestrator never writes code or runs commands directly.
- **Maximize parallelism.** Independent tasks always run concurrently.
- **Full context per dispatch.** Each subagent receives a self-contained task with all necessary information.
- **Iterate until professional quality.** Hard cap of 5 iteration rounds.

## File Structure

```
.
├── agent.md                  # Orchestrator definition (Cursor command)
├── subagents/
│   ├── debugger.md           # Targeted fixer
│   ├── designer.md           # Visual deliverable creator
│   ├── executor.md           # General-purpose implementer
│   ├── file-explorer.md      # Document extraction & organization
│   ├── qa-specialist.md      # Output quality inspector
│   └── verifier.md           # Per-item checker
└── iterations/               # Development logs and self-reflections
```

## Setup

These files are designed as [Cursor IDE](https://cursor.com/) agent definitions:

- `agent.md` → Place at `~/.cursor/commands/agent.md` (custom command)
- `subagents/*.md` → Place at `~/.cursor/agents/` (subagent definitions)

## Model Selection

Each subagent dispatch supports a `model` parameter:

| Role | Default Model | Upgrade When |
|------|--------------|--------------|
| executor | fast | Complex or core tasks affecting product quality |
| designer | fast | Complex multi-step design |
| QA Specialist | default (full) | Use fast for lightweight/intermediate checks |
| verifier | fast | — |
| debugger | fast | Complex multi-file fixes |
| file-explorer | default | — |
