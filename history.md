# Version History

## v1 (2026-03-10)

Initial release of the multi-agent orchestration system.

### Core Features

- **Orchestrator pattern**: Tech-lead agent that plans, delegates, and manages quality. Never writes code directly.
- **6 specialized subagents**:
  - `executor` — General-purpose implementation (code, commands, tests, setup)
  - `designer` — Visual deliverables (PDF via LaTeX/HTML, web pages, slides) with build-validate-fix loop
  - `debugger` — Scoped fixes from QA issue lists, restricted to allowed files
  - `qa-specialist` — Read-only output inspection, Full and Lightweight modes
  - `verifier` — Fast per-item PASS/FAIL checks against explicit criteria
  - `file-explorer` — Document extraction and organization (PDF, DOCX, PPTX)
- **QA closed loop**: QA Specialist -> Debugger -> Verifier -> re-QA (max 3 rounds)
- **Task sizing**: S/M/L classification with corresponding workflows
- **Parallel dispatch**: Independent tasks always run concurrently
- **Model selection**: Per-dispatch fast/default model choice to balance cost and quality
- **Iteration control**: Structured review after each round, hard cap of 5 rounds
- **Self-contained task format**: Each subagent dispatch includes full context (zero shared memory)
