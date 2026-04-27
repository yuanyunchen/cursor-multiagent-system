---
name: write-report
description: "Professional LaTeX PDF report writing for report-writer. Guides content organization, evidence-backed writing, local template selection, and LaTeX source preparation."
---

# Write Report

Use this skill when `report-writer` produces, rewrites, or polishes a professional LaTeX PDF report.

This skill covers report content and LaTeX template work. The `report-writer` subagent owns the build, visual inspection, iteration loop, evidence lifecycle, and final cleanup.

## Core Workflow

1. Audit whether the supplied context is enough to write a truthful report.
2. Choose the closest local LaTeX starter or task-provided official template.
3. Shape the report around the audience, evidence, venue, and any requested sections.
4. Write clean LaTeX with real figures, tables, citations, and cross-references.
5. Hand the source to `report-writer`'s build and QA loop.

## Context Sufficiency

Before drafting, confirm that the task includes the information needed to support the report:

- purpose, audience, and required deliverable type;
- original requirements, rubric, venue, publisher, or page constraints;
- methods, assumptions, implementation choices, and evaluation criteria;
- result files, metrics, figures, tables, logs, or source data for claims;
- interpretation notes that explain what the results mean;
- requested or expected sections, citation style, and source paths for required assets.

When important information is missing, return this exact structure to the orchestrator:

```markdown
## NEEDS_MORE_CONTEXT

### Missing Items
1. **{item}** - why the report needs it and the expected file/path/type.

### Requested Orchestrator Action
- {compute / extract / clarify with user / collect file / run evaluation / summarize results}

### Can Continue After
- {specific condition that unblocks writing}
```

Resume only after the missing material is supplied, then run the audit again.

## Report Shape

Select sections for the task instead of using a fixed outline. The examples below are starting points: keep, merge, rename, reorder, or omit sections based on the audience, evidence, and deliverable purpose.

For professional technical reports, consider:

1. Title page
2. Executive summary
3. Problem statement and objectives
4. Requirements or evaluation criteria
5. Method or system design
6. Experimental setup, data, or implementation details
7. Results
8. Analysis and interpretation
9. Limitations and risks
10. Recommendations or next steps
11. Conclusion
12. References
13. Appendix

For academic papers, adapt to the venue. Common sections include abstract, introduction, related work when useful, method, experiments, results, discussion, limitations, conclusion, references, and appendix.

For business or decision reports, prioritize the decision context, findings, evidence, implications, and recommendations; use only the sections that help the reader make the decision.

## Writing Standards

- Tie major claims to supplied evidence, cited sources, or clearly labeled assumptions.
- Explain the meaning of results; convert raw outputs into conclusions and implications.
- Use precise terminology and define task-specific concepts.
- Give figures and tables takeaway-focused captions.
- Reference every important section, figure, table, equation, and appendix from the text.
- State limitations candidly and connect them to risk or future work.
- Keep paragraphs concise and topic-driven.

## Figures, Tables, And Equations

Figures should use real supplied assets or generated plots from supplied data. Make labels, legends, units, and captions readable in the final PDF.

Tables should be native LaTeX tables with meaningful row/column labels, units, and clean numeric alignment. Prefer `booktabs` for professional reports.

Equations should be numbered and referenced when they are central to the method or analysis. Keep code snippets short in the main text and move long listings to an appendix.

If a required figure, table, metric, or source file is missing, request context instead of filling the gap.

## Template Selection

Use the first applicable option:

1. Task-provided official template files.
2. Local ready-to-use starter in `templates/<scenario>/`.
3. Updated official author kit cached into `templates/<scenario>/` when a named venue/publisher requires the latest template.
4. CTAN / TeX Live class starter when no venue-specific files are required.

Local starters are preprocessed to avoid redundant author-kit files. Each scenario should contain only the source files needed to start a report, usually `main.tex`, `references.bib`, `README.md`, and any local style files required by that scenario.

`templates/manifest.json` records:

- `scenario`
- `template_dir`
- `source_type`: `local-default`, `local-starter`, `official`, `ctan`, `community`, or `task-provided`
- `freshness`: `offline-default`, `pinned`, `check-latest`, or `stale`
- `last_checked`
- `notes`

For `check-latest` or `stale` entries tied to a named submission venue, refresh from the official author instructions before writing and update the manifest. For generic/internal reports, use the local starter directly.

## Scenario Routing

| Scenario | Local Starter | Use |
|----------|---------------|-----|
| General professional report, technical report, lab report | `templates/generic-professional/` | Default polished multi-section report. |
| Short academic article / internal research note | `templates/academic-article/` | Article-like work without publisher constraints. |
| IEEE journal / conference / engineering paper | `templates/ieee/` | IEEE-style work; refresh for named IEEE submissions. |
| ACM paper / SIG proceedings | `templates/acm/` | ACM-style work; refresh for named ACM submissions. |
| Springer Nature journal | `templates/springer-nature/` | Springer Nature journal work; confirm journal style. |
| Springer LNCS / LNAI / LNBI proceedings | `templates/springer-lncs/` | LNCS-style proceedings. |
| Elsevier journal | `templates/elsevier/` | Elsevier-style journal work; confirm target journal style. |
| CVPR-style paper | `templates/cvpr/` | CVPR-style work; refresh for named CVPR submissions. |
| ICLR-style paper | `templates/iclr/` | ICLR-style work; refresh for named ICLR submissions. |
| Thesis / book-like long report | `templates/thesis-like/` | Long report fallback when no university template is required. |

## Build Entry Points

Use Tectonic for most single-source reports:

```bash
tectonic main.tex
```

Use `latexmk` when the report needs repeated runs, BibTeX, indexes, glossaries, or complex references:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Use BibTeX-compatible bibliography styles unless the environment is confirmed to support `biblatex`/`biber`.

For markdown-to-LaTeX conversion tasks, use the local helper only for supported local templates:

```bash
python ~/.cursor/skills/write-report/scripts/build.py \
  --mode tex \
  --template iclr \
  --input content.md \
  --figures figures \
  --output report.pdf
```

## Output Principle

The LaTeX source is the report's source of truth. Deliver a complete, evidence-backed, professionally structured report with no placeholder narrative, no unsupported results, and no template instructional text in the final document.
