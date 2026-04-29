# Version History

## Unreleased

### 2026-04-28 — Executor Skills-first: inline `parallel-*` defaults; merge overlap-routing into Rule 1

Three table-side notes that lived as separate paragraphs after the executor Skills table got tighter homes:

- **Research depth defaults** (`agentic` for `parallel-web-search`, `ultra` for `parallel-deep-research`) inlined into the trigger column of the corresponding rows — they belong to the skill choice, not the file.
- **`parallel-*` Glob resolution** collapsed to a one-line footnote (`†`) below the table; the skills live in a plugin cache whose path contains a commit SHA, so the executor still needs the resolution recipe somewhere — but it is metadata, not policy.
- **Routing-when-triggers-overlap** absorbed into Rule 1 (Skills-first). One rule for one decision; saves a rule slot and removes the prose-vs-rule split.

Net change: `executor.md` 62 → 58 lines (−4). No behavior change for downstream consumers; same triggers, same defaults, same overlap policy.

#### Files Modified

- `core/subagents/executor.md`
- `history.md` (this entry)

No deploy / no archive (log-only).

### 2026-04-28 — Skills-first: rename sections, hoist before Task Input, add Rule 1

Follow-up to the previous entry. Two changes for human readability and explicit prioritization:

1. **Section rename + position.** `## Skills (read first when applicable)` → `## Skills-first`, hoisted to immediately after the role paragraph (before `## Task Input`) in `executor`, `debugger`, `qa-specialist`, `report-writer`, `file-extractor`. `frontend-engineer` keeps its existing position (after `## Task Input`) because it sits before `## Routing`, which depends on the Skills section. All Skills-first sections now open with a bold imperative ("Before X, scan / read…").
2. **Skills-first as Rule 1.** Every subagent with a Skills-first section now has `Rule 1: Skills-first` at the top of `## Rules`, in addition to the section itself. Surfacing it twice — once in dedicated section, once in the Rules list — is intentional; this is a high-value rule and Rules sections are scanned at decision points where Skills-first must trigger first.

`verifier` unchanged (no skills apply to read-only code review).

#### Side effects

- `executor` Rules renumbered 1→7 (was 1→6).
- `debugger` Rules renumbered 1→6 (was 1→5).
- `qa-specialist` Rules renumbered 1→10 (was 1→9). The Skills-first section's "Rule 4 violation" cross-reference replaced with a direct phrasing ("violates the exhaustive-not-sampled rule below") to avoid renumber drift.
- `report-writer` Rule 2 ("Skill owns mechanics") absorbed into new Rule 1 ("Skills-first"); Rules now 1→3.
- `file-extractor` Rules renumbered 1→9 (was 1→8).
- `frontend-engineer` Rules renumbered 1→10 (was 1→9); the in-body "(Rule 9)" reference for missing `<output_dir>` updated to "(Rule 10)".

#### Files Modified

- `core/subagents/executor.md`
- `core/subagents/debugger.md`
- `core/subagents/qa-specialist.md`
- `core/subagents/report-writer.md`
- `core/subagents/file-extractor.md`
- `core/subagents/frontend-engineer.md`
- `history.md` (this entry)

No deploy / no archive (log-only).

### 2026-04-28 — Skills-first subagents: per-subagent Skills tables; fix `file-extractor` Initialize-only claim

Make subagents skills-first: each subagent declares the skills it must read first when its triggers match. Orchestrator (`agent.md`) intentionally NOT given a global skills table — routing-by-deliverable-type stays implicit via subagent descriptions. Also fixes `file-extractor`'s "Initialize-only" claim, which contradicted Step 5's `NEEDS_MORE_CONTEXT` loop in `agent.md` line 113 and `file-extractor`'s own description.

#### Changes

- **`agent.md`** — `<team>` row for `file-extractor` corrected: "Initialize-only" → "Primary use in Initialize…; also in Step 5 `NEEDS_MORE_CONTEXT` loop when a producer needs additional source material extracted." Aligns with workflow Step 5.
- **`core/subagents/file-extractor.md`** — frontmatter description corrected (same fix as above); `## Extraction Skills` section renamed `## Skills (read first when applicable)` and table headers normalized to `Trigger | Skill | Path` for consistency with the new pattern in other subagents. Rule 4 wording updated accordingly.
- **`core/subagents/executor.md`** — new `## Skills` section (11 triggers) covering `pdf`, `docx`, `pptx`, `xlsx`, `file-content-extraction`, `webpage-content-extraction`, `webapp-testing`, and the four `parallel-*` research/extraction skills. Research-depth defaults explicitly stated: `parallel-web-search` → `agentic` (only `fast` when `<parameters><speed>fast</speed>`); `parallel-deep-research` → `ultra` by default. `parallel-*` paths resolved via `Glob` since the plugin cache directory contains a commit SHA. Routing rule for overlapping triggers spelled out.
- **`core/subagents/qa-specialist.md`** — new `## Skills` section (5 triggers: PDF / `.pptx` / `.docx` / `.xlsx` / web). Old inline "For PDF outputs: use `file-content-extraction` skill at …" line in Full Mode workflow replaced with a generic "drive the inspection through the matching skill from the Skills table above" — single source of truth.
- **`core/subagents/report-writer.md`** — single `write-report` reference promoted to a `## Skills` table that also lists `file-content-extraction` (final-pass page render for self-QA) and `pdf` (manipulating produced PDFs). Rule 2 hardcoded path replaced with reference to the Skills table.
- **`core/subagents/debugger.md`** — new `## Skills` section with one trigger (`webapp-testing` for reproducing browser bugs).
- **`core/subagents/frontend-engineer.md`** — unchanged (already had a Skills table from a prior version).
- **`core/subagents/verifier.md`** — unchanged (no skill applies to read-only code review).

#### Rationale

User decision: skills are exposed to subagents only, not duplicated into a global `<skills>` table on `agent.md`. Subagent files remain independent modules (Rule 6); each owns the list of skills it must consult. Main agent routes by deliverable type (the existing implicit mechanism in `<team>`); skill resolution happens inside the chosen subagent.

The `file-extractor` "Initialize-only" wording was a stale claim — Step 5's `NEEDS_MORE_CONTEXT` loop has been calling `file-extractor` since v3.x. Triaged as "stale or factually wrong" per the `write-agent-file` skill, fixed in the same change.

Executor research defaults (`agentic` for search, `ultra` for deep research) were specified explicitly so the subagent does not silently downgrade to `fast` when latency-sensitive paths are not actually requested.

#### Files Modified

- `core/agent.md` (1 line edit, file-extractor team row)
- `core/subagents/executor.md` (+25 lines)
- `core/subagents/qa-specialist.md` (+13 lines, −1 inline)
- `core/subagents/report-writer.md` (+8 lines, −1 inline)
- `core/subagents/debugger.md` (+8 lines)
- `core/subagents/file-extractor.md` (header rename, table reformat)
- `history.md` (this entry)

No deploy / no archive (log-only). README unchanged — public capabilities and workflow not affected, only subagent-internal routing of mechanical layers.

### 2026-04-28 — Apply `write-agent-file` skill review to all `core/subagents/*.md`

Internal-only review pass: dedup duplicate report-structure sections, delete filler rules, fix Rule 6 cross-reference violations, drop hardcoded environment paths. No agent capability or workflow change — `README.md` intentionally not updated. Total: 642 → 595 lines (−47) across the seven subagent files.

#### Changes

- **`report-writer.md`** — description and body no longer name `frontend-engineer` for non-PDF deliverables (violated `agent.md` Rule 6 "subagents are independent modules"). Body now states scope and defers routing to the orchestrator.
- **`frontend-engineer.md`** —
  - Removed hardcoded fallback path `cursor-multiagent-system/results/current/deliverables/{name}/`; missing `<output_dir>` is now a Rule 9 blocker (orchestrator owns paths per `agent.md` Rule 6).
  - Removed hardcoded macOS Chrome binary path (`/Applications/Google Chrome.app/...`) and the inline `chrome --headless` example; both delegated to the `webapp-testing` skill.
  - Consolidated "design intentionality" repetition: folded former Rule 5 (AI-slop anti-patterns) into Rule 2; deleted former Rule 11 (no placeholders) and merged its content into Rule 1 ("ship-ready"). Renumbered remaining rules; fixed dangling "Rule 10" reference to "Rule 9".
- **`executor.md`** — Option C consolidation:
  - Former Rule 1 ("always seek the better solution") + Rule 3 ("minimal change when modifying existing code") merged into a single Rule 1 keyed to work type (existing code → smallest diff + match style; new modules → best architecture).
  - **Pre-existing issues in touched code must now appear in the return message** — added explicit clause to Rule 1 and to the "message back to the orchestrator" paragraph. Out-of-scope issues spotted during work are reported, not fixed, and never silently dropped.
  - Deleted Rule 5 ("Read before write") and Rule 7 ("No placeholders") as capable-agent defaults that change no behavior.
  - De-named "verifier/QA" in the Documentation handoff text → "the next reviewer" (`agent.md` Rule 6 hygiene).
- **`verifier.md`** — merged the duplicate "Output Format" and "Documentation" sections (had drifted: Documentation listed Scope / Requirements check / Overview, Output Format did not). Single canonical schema now embedded in Output Format.
- **`qa-specialist.md`** — merged duplicate "Output Reference Structure" + "Documentation" sections; tightened role paragraph (removed redundant restatements of "never read code", which was repeated four times across role / Modes / Rule 1 / Rule 9); folded former Rule 5 ("Actually look at content") into Rule 4 ("Exhaustive, not sampled").
- **`debugger.md`** — merged duplicate "Output Format" + "Documentation" sections; folded former Rule 6 ("Match style") into Rule 2 ("Minimal change"); deleted standalone Rule 5 ("No placeholders") and merged into the new Rule 5 ("No placeholders, no incomplete fixes"); description no longer points to "Verifier or QA Specialist" (Rule 6 violation), now refers generically to "a code review or QA pass".

#### Rationale

`agent.md` Rule 6 explicitly forbids subagent files from naming sibling subagents, but `report-writer.md` and `debugger.md` did so in their YAML descriptions, and `frontend-engineer.md` carried hardcoded absolute paths that violated "orchestrator owns layout, paths". Several files also had `Output Format` + `Documentation` sections describing the same report schema in different words — a textbook drift hazard per the `write-agent-file` skill's single-source-of-truth principle. The executor Rule 1 vs Rule 3 tension ("always seek the better solution" vs "minimal change") was a true principle conflict — Option C (one rule keyed to work type) resolves it without losing either intent, and the new return-message requirement closes the loophole where executors notice rot in existing code but never surface it.

#### Files Modified

- `core/subagents/debugger.md` (49 → 47 lines)
- `core/subagents/executor.md` (40 → 36 lines)
- `core/subagents/frontend-engineer.md` (175 → 167 lines)
- `core/subagents/qa-specialist.md` (105 → 102 lines)
- `core/subagents/report-writer.md` (82 → 82 lines, content edits only)
- `core/subagents/verifier.md` (85 → 84 lines)
- `history.md` (this entry)

`core/subagents/file-extractor.md` and `core/agent.md` reviewed but not edited (no violations found / user deferred orchestrator sync).

#### Tested On

- `ReadLints` clean across all six modified files.
- Cross-checked all rule-number references inside each file after renumbering — only one stale ref found (`frontend-engineer.md` "Rule 10") and fixed in the same pass.
- Cross-checked subagent descriptions against the `<team>` table in `core/agent.md`: capabilities, mode names (`Full | Format | Lightweight` for qa-specialist, `Full | Polish` for frontend-engineer), and dual-use flagging all consistent.

## v2.6.7 (2026-04-28)

Add a "log-only changes" sub-protocol to `llm.md` for accumulating small parallel-agent edits without bumping a version on every one.

### Changes

- **`llm.md` Git & Versioning** — new sub-protocol "Log-only changes (no version bump)" added after the commit protocol. Triggered by phrases like "log change" / "记录改变" / "不更新版本号" / "log only". Reuses the commit protocol with two differences: no version bump (skip Step 1) and no deploy / archive (skip Step 4). Entries accumulate under a `## Unreleased` section at the top of `history.md` with `### <date> — <summary>` sub-headings; commit message uses `log:` prefix instead of `v<N>:`. At the next real version bump, the `Unreleased` items merge into that version's entry. The use case is multiple agents editing in parallel where individual edits don't each warrant a version.

### Rationale

When several agents work on the system in parallel without coordinating, every small edit getting its own version produces churn (deploy + archive + history entry per micro-change) that bypasses the value of versioning. Log-only entries let small changes accumulate under `Unreleased` and only get promoted to a real version when a coherent set is ready. **Internal-only protocol change** — affects how agents log work, not what the runtime system does — so `README.md` is intentionally not updated.

### Files Modified

- `llm.md`
- `history.md` (this entry)
- `iterations/README.md` (v2.6.7 row added; gitignored)

### Tested On

- The new sub-protocol is itself self-applying: this version bump (v2.6.7) is the right path for a workflow change, while future micro-edits would correctly take the log-only path. Both paths cross-reference consistently.

## v2.6.6 (2026-04-28)

Apply `write-agent-file` skill review to `llm.md`: fix two stale archive-scope statements and dedup one description block. Internal-only documentation refactor — no agent capability or workflow change.

### Changes

- **L130 (commit protocol Step 4)** — archive description was still listing the pre-v2.6.4 scope (`core`, `skills`, `scripts` only). Updated to enumerate all five archived items (`core/`, `skills/`, `scripts/`, `llm.md`, `README.md`) and cross-reference the "Per-version archive" section for the layout.
- **L15 (workspace tree comment)** — `scripts/deploy.sh` comment was ambiguous about sync-vs-archive scope. Rewritten as: "Deploys core/+skills/ to ~/.cursor/; --archive [<v>] snapshots all source state to iterations/v<N>/files/" — making clear that sync targets two dirs while archive captures everything.
- **Phase 3 (Version Transition)** — full prose duplicating commit protocol Step 4 collapsed into a one-line reference: "Run the deploy step from the commit protocol above (`./scripts/deploy.sh --archive v<N>`) to populate `iterations/v<N>/files/`. Diff to verify deployed files match source." Single source of truth for the deploy command now lives in Step 4.

### Rationale

After v2.6.4 expanded the archive scope to include `llm.md` and `README.md`, two locations in `llm.md` continued to describe the old three-dir scope, creating drift between the workflow rules and the actual `deploy.sh` behavior. Internal-only — no change to agent capabilities or workspace conventions visible at runtime — so `README.md` is intentionally not updated.

### Files Modified

- `llm.md`
- `history.md` (this entry)
- `iterations/README.md` (v2.6.6 row added; gitignored)

### Tested On

- `./scripts/deploy.sh --archive v2.6.6` — all five items written.
- Cross-checked all `llm.md` mentions of the archive scope; only the three statements above were stale, all now consistent with the canonical "Per-version archive" section (L88-95).

## v2.6.5 (2026-04-28)

Back-fill missing version entries in `history.md` so every version listed in `iterations/README.md` (and every user-curated archive folder) has a narrative entry. Internal-only documentation refactor — no agent capability or workflow change.

### Changes

- **`history.md` v1.0 entry** added — user-curated archive (no commit mapping). Describes the pre-formal-versioning prototype state captured into `iterations/v1.0/files/`; reconstructed from the earliest tracked commit `010045c` and archive contents.
- **`history.md` v1.1 entry** added — user-curated archive. Documents the first iteration cycle on the v1 prototype: end-to-end run on `cv2-homework3` that produced the project's first reflection, code review, human feedback, problems, and requirements artifacts (all preserved under `iterations/v1.1/`).
- **`history.md` v1.2 entry** added — reconstructed from commit `7af8efc` body (model selection simplification, workspace overhaul, quality pipeline reorder, deploy script `--archive` flag, honest-assessment summary rule). The original commit predates the v2.1.2 commit protocol that made history-entry updates mandatory; this entry is back-filled from the commit message.

### Rationale

Three versions had archive folders or commits but no narrative entry, breaking the "every version is self-describing" property that `iterations/README.md` and the per-version archive policy assume. Internal-only — no change to agent capabilities or workflow visible at runtime — so `README.md` is intentionally not updated.

### Files Modified

- `history.md` (this entry plus v1.0, v1.1, v1.2 back-fills)
- `iterations/README.md` (v2.6.5 row added; gitignored)

### Tested On

- `./scripts/deploy.sh --archive v2.6.5` — all five archive items written.
- `grep "^## v" history.md` confirms entries for all 22 versions in `iterations/README.md` plus the three user-curated v1.0 / v1.1 / v1.5 archives.

## v2.6.4 (2026-04-28)

Per-version archive scope expanded to include `llm.md` and `README.md`. Every `iterations/v<N>/files/` snapshot now reconstructs the workflow rules and public-facing docs alongside the source dirs. Internal-only refactor of the archive policy — no agent capability change.

### Changes

- **`scripts/deploy.sh`** — `--archive` step now copies `llm.md` and `README.md` into `iterations/<version>/files/` alongside `core/`, `skills/`, `scripts/`. Header comment updated to document the new layout.
- **`llm.md`** — Workspace structure tree updated (per-version `files/` now lists all five items). "Per-version archive" section rewritten to enumerate the archive contents and explain why workspace docs are included (workflow rules and public-facing docs reconstructible alongside code). One-line description in the workspace tree updated to match.
- **Historical back-fill** — `iterations/v<N>/files/llm.md` and `README.md` populated for every committed version mapped in `iterations/README.md` (v1 through v2.6.3). Source: `git show <sha>:llm.md` / `git show <sha>:README.md` for the commit recorded in the version → commit-SHA index. v1 had no `llm.md` (added in v1.2), so v1 only gets `README.md`. The user-curated archives `v1.0/`, `v1.1/`, `v1.5/` are intentionally untouched (no matching commit, per the existing `iterations/README.md` "User-curated archives" note).

### Rationale

Workflow rules (`llm.md`) and public-facing capability docs (`README.md`) evolve in lockstep with the agent definitions. Without them in the per-version archive, restoring `iterations/v<N>/files/` reconstructs only the runtime behavior, not the protocol that produced it. This is **internal-only** to the archive policy — no change to agent capabilities, dispatch protocol, or workspace conventions visible to a runtime task — so `README.md` is intentionally not updated.

### Files Modified

- `scripts/deploy.sh`
- `llm.md`
- `history.md` (this entry)
- `iterations/v<N>/files/llm.md` and `iterations/v<N>/files/README.md` for v1, v1.2, v1.3, v2, v2.1, v2.1.1, v2.1.2, v2.2, v2.3, v2.3.1, v2.4, v2.4.1, v2.4.2, v2.4.3, v2.5, v2.6, v2.6.1, v2.6.2, v2.6.3 (gitignored, local only)
- `iterations/README.md` (v2.6.4 row added; gitignored)

### Tested On

- `./scripts/deploy.sh --archive v2.6.4` — all five items written to `iterations/v2.6.4/files/`: `core/`, `skills/`, `scripts/`, `llm.md`, `README.md`.
- Back-fill loop verified: v1 correctly skipped `llm.md` (file did not exist at that commit) while writing `README.md`.

## v2.6.3 (2026-04-28)

Apply `write-agent-file` skill review to `core/agent.md`: clarify Rule 2 user-interaction semantics, surface Rule 1 vs Rule 2 conflict, dedup repeated information, slim `<team>` table to pure routing, and tighten layout. Internal-only refactor — no capability or workflow change.

### Changes

- **Rule 2 rewrite** — recast as three-part user-interaction contract: self-solve first (debug / retry / dispatch / redesign), escalate only when the user must intervene, never silently exit early or substitute deviating results. Replaces the previous prose that mixed value framing with action.
- **Rule 1 clarification** — appended one sentence resolving the Rule 1 (never read code) vs Rule 2 (self-solve) tension: when self-solving requires looking at code or runtime state, dispatch `explore` or `verifier` rather than reading directly.
- **`<parameters>` decision rule** — added single-line decision rule for the composer-2 vs inherit choice, removing the gray zone between Rule 4 (quality-first) and the cost default.
- **`<team>` table slimmed** — dropped per-row internal-loop / QA-evidence / output-path detail and Writes notes; retained agent + type + 1–2-sentence use case + mode names. Footer states the internal-QA-satisfies-module-close rule once and points to `<workspace>` Naming conventions for paths.
- **Dedup pass** — single source of truth for: `brief.md` description (removed duplicate dispatch-norms reminder), `<task_format>` `<report>` field (now references Naming conventions), Step 4 hygiene prose (now "Run hygiene pass per Rule 8"), and the team-row Writes annotations.
- **Cleanup** — removed Rule 4 value-as-rule preamble ("Bar = strong senior-engineer solution"), removed `<summary_format>` redundant trailing instruction, simplified Step 1.1 prose by referencing `<workspace>`. Operational priorities under Rule 1 converted to numbered list.
- **Grammar fixes** — Step 3.2 sentence fragment ("add `verifier` for code-heavy core ones") capitalized and clarified to "Add `verifier` for code-heavy core modules"; Step 5 first bullet trailing period restored.

### Rationale

This is an **internal-only refactor** — no change to agent capabilities, dispatch protocol, workspace layout, or public-facing docs — so `README.md` is intentionally not updated.

### Files Modified

- `core/agent.md`
- `history.md` (this entry — back-filled, see note below)
- `iterations/README.md` (v2.6.3 row added; not in git per `.gitignore`)

### Tested On

- Whole-file consistency check per `llm.md` Agent Design Principle 5: `<role>` ↔ `<rules>` ↔ `<workflow>` mutually consistent; `<team>` rows match each subagent's YAML; `<task_format>` field usage unchanged; Naming conventions table unchanged.
- `./scripts/deploy.sh --archive v2.6.3` — deployed to `~/.cursor/` and snapshotted to `iterations/v2.6.3/files/{core,skills,scripts}/`.

### Note: back-filled

The agent.md changes themselves landed in commit `68a52d4` (`refactor(agent.md): apply write-agent-file skill review`) without a `v<N>:` tag and without a corresponding `history.md` entry. This `v2.6.3` entry back-fills the missing protocol artifacts (history entry, version archive, `iterations/README.md` row mapping `v2.6.3 → 68a52d4`). Per `llm.md` commit protocol, past entries are never modified; the back-fill itself is committed in a follow-up commit.

## v2.6.2 (2026-04-27)

Per-version archive policy clarified; `deploy.sh --archive` accepts a version target so every commit produces a reconstructible snapshot.

### Changes

- **`scripts/deploy.sh`** — `--archive` now accepts an optional `<version>` argument. With no arg, snapshots to `iterations/current/files/` (old behavior). With a version, snapshots to `iterations/<version>/files/{core,skills,scripts}/`. Archive now also excludes `__pycache__`, `*.pyc`, `.DS_Store` so snapshots stay clean.
- **`llm.md` commit protocol** — rewritten as a 7-step checklist that makes per-commit archival mandatory: every commit (including patches) runs `./scripts/deploy.sh --archive v<N>` so the version is reconstructible from `iterations/v<N>/files/` without reaching into git history. Adds explicit guidance on when to update `README.md` (user-facing capability change) vs skip it (internal refactor — record rationale in `history.md`). Adds a `history.md` back-fill rule for missed past commits.
- **`llm.md` "Iterations" section** — split into "Per-version archive" (frozen `v<N>/files/`) and "In-progress artifacts" (working `current/`). Documents the new ad-hoc `current/archive/<date>_<topic>/` slot for local-only snapshots that don't correspond to a commit.
- **`llm.md` Version Transition Phase 4** — updated to preserve the already-populated `iterations/v<N>/files/` from Phase 3 instead of overwriting it; only non-`files/` artifacts move from `current/` to `v<N>/`.
- **`iterations/README.md`** — version → commit-SHA index now explicitly part of the commit protocol (Step 5).

### Rationale

This is an **internal-only refactor** of the development workflow — no change to agent capabilities, runtime behavior, or public-facing docs — so `README.md` is intentionally not updated.

### Files Modified

- `scripts/deploy.sh`
- `llm.md`
- `history.md` (this entry)
- `iterations/README.md` (v2.6.2 row added; not in git per `.gitignore`)

### Tested On

- `./scripts/deploy.sh --archive v2.6.1` — wrote correctly to `iterations/v2.6.1/files/{core,skills,scripts}/`; verified diff against `current/files/` is exactly `scripts/deploy.sh` (expected — v2.6.1 has the old script, current has the new one).

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

## v1.0 (2026-03-10) — user-curated archive, no commit mapping

Pre-formal-versioning prototype state. Captured into `iterations/v1.0/files/` by hand before the version log existed; the `iterations/README.md` "User-curated archives" section is the authoritative note. Reconstructed here from the earliest tracked commit `010045c` (init: General Coding Agent system) and the v1.0 archive contents.

### Archive contents (`iterations/v1.0/files/core/`)

- `agent.md` — first orchestrator definition.
- `subagents/` — initial 6 subagents: `executor`, `designer`, `debugger`, `qa-specialist`, `verifier`, `file-explorer`.

### Notes

- Predates `llm.md` (added later in commit `5c3f4ce`) and the `history.md` log itself (introduced with v1, commit `5525320`).
- No git commit corresponds 1:1 to this archive snapshot — it is the user-saved state at some point during the early prototype phase. Treat as historical reference only; not reconstructible from a single SHA.

## v1.1 (2026-03-10) — user-curated archive, no commit mapping

First iteration cycle on the v1 prototype: the `cv2-homework3` task was run end-to-end, producing the project's first reflection / code review / human feedback / problems / requirements artifacts. Captured by hand under `iterations/v1.1/`; no matching git commit (predates the formal commit protocol).

### Archive contents (`iterations/v1.1/`)

- `files/core/` — agent definitions at this stage (still 6 subagents, pre-`llm.md`).
- `cv2-homework3_self_reflection.md` — first end-to-end self-reflection on a real task.
- `code_review.md` — first code review of `general-coding-agent v1`.
- `human_feedback.md` — first user observations from runs.
- `problems.md` — first consolidated problem list (sourced from the three artifacts above).
- `requirements/` — early requirements drafts: `cost aware and model selection.md`, `plann & reflect & file system.md`.

### Notes

- These artifacts seeded the design pressure that led to v1.2 (model selection simplification, workspace overhaul, quality pipeline reorder) and v1.5 (orchestrator never reads code, report-writer renaming, verifier redesign).
- Like v1.0, no git SHA represents this snapshot exactly; the file system is the authoritative record.

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

## v1.2 (2026-03-12)

Major simplification and refinement (commit `7af8efc`). Reconstructed from commit message body — entry was missing from the original log.

### Changes

- **Simplify model selection to fast / inherit** (Cursor Task tool constraint). Removed the multi-tier model selection that v1 originally had.
- **Workspace overhaul.** Removed `dispatches/`, added `documents/`, replaced `analysis/` with `standards/`. Set the directory structure that later versions iterate on.
- **Reorder quality pipeline** to Verifier → Debug → QA → Designer (from v1's QA → Debug → Verify → re-QA loop).
- **Execute–verify–QA loop with three gate levels per sub-module.** First explicit per-module gating model.
- **Verifier may fix obvious issues**; all QC agents do holistic review (not pure checklist tickers anymore).
- **Principle-based task splitting** — Rule 3 rewritten away from S/M/L sizing toward principle-driven decomposition.
- **Autonomous execution** — orchestrator no longer requires user confirmation for plans before executing.
- **Output containment, scope isolation, delegation autonomy** — three new rules on what the orchestrator does and does not do.
- **Designer may trim / rephrase for layout conventions** (limited content edits permitted in service of formatting).
- **Deploy script `--archive` flag** introduced; `current/`-first versioning workflow established.
- **Honest assessment in delivery summary** — first formalization of the "do not hide unresolved issues" rule that later evolves into v2.4's mandatory bulleted summary.

### Files Modified

- `core/agent.md` — major rewrite (model selection, rules, workflow).
- `core/subagents/*.md` — per-subagent updates aligned with the new pipeline order and behaviors.
- `scripts/deploy.sh` — `--archive` flag added.
- `llm.md` — `current/`-first workflow documentation.
- `history.md` — back-filled in this entry (commit `7af8efc` did not include a v1.2 history entry; rule was not yet established).

### Note: back-filled

Commit `7af8efc` predates the v2.1.2 commit protocol (which made `history.md` updates mandatory). This entry is reconstructed from the commit message body; it is not a contemporaneous log.

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
