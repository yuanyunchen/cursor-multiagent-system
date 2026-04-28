---
name: write-report
description: "LaTeX engineering and tooling layer for report-writer. Owns template inventory, document-class baselines, package stack, build/render commands, and the formatting rules LLMs commonly miss. Does not judge content."
---

# Write Report

Mechanical reference for `report-writer`. Content judgment lives in `report-writer.md`.

## Template Selection

1. Task-provided official files.
2. Local starter under `templates/<scenario>/`.
3. Latest official kit cached into `templates/<scenario>/` and recorded in `manifest.json` (named venues only).
4. CTAN class as last resort.

`manifest.json` fields: `scenario`, `template_dir`, `source_type` (`local-default | local-starter | official | ctan | community | task-provided`), `freshness` (`offline-default | pinned | check-latest | stale`), `last_checked`, `notes`. For named submissions with `check-latest` or `stale`, refresh from the official author kit and update the manifest before writing.

## Scenario Routing

| Scenario | Local Starter | Main file | Document class | Bib backend | Two-column |
|---|---|---|---|---|---|
| Generic / technical / lab report | `templates/generic-professional/` | `main.tex` | `scrartcl` (KOMA) | `natbib` | no |
| Short academic article | `templates/academic-article/` | `main.tex` | `article` | `natbib` | no |
| IEEE journal / conference | `templates/ieee/` | `main.tex` | `IEEEtran` | `IEEEtran` bst | yes |
| ACM paper / SIG | `templates/acm/` | `main.tex` | `acmart` | `biblatex` (acm) | varies |
| Springer Nature journal | `templates/springer-nature/` | `main.tex` | `sn-jnl` | `biblatex` | no |
| Springer LNCS / LNAI / LNBI | `templates/springer-lncs/` | `main.tex` | `llncs` | `splncs04` bst | no |
| Elsevier journal | `templates/elsevier/` | `main.tex` | `elsarticle` | `model1-num-names` bst | varies |
| CVPR-style | `templates/cvpr/` | `main.tex` | `article` + `cvpr.sty` | `ieeenat_fullname` bst | yes |
| ICLR-style | `templates/iclr/` | `main.tex` | `article` + `iclr2025_conference.sty` | `iclr2025_conference` bst | no |
| Thesis / book-like | `templates/thesis-like/` | `main.tex` | `scrreprt` (KOMA) | `biblatex` | no |

## LaTeX Engineering Baseline

LLMs frequently miss these specific choices; load packages in this order to avoid clashes:

```latex
\usepackage{microtype}
\usepackage{graphicx}        \graphicspath{{figures/}}
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{siunitx}
\usepackage{amsmath, amssymb}
\usepackage[hidelinks]{hyperref}
\usepackage[capitalize]{cleveref}   % after hyperref
\usepackage{subcaption}             % NOT subfig
\usepackage{listings}               % or minted; pick one
\usepackage{xcolor}
```

- **Encoding.** Tectonic defaults to UTF-8. For pdflatex paths only, add `\usepackage[T1]{fontenc}` and `\usepackage[utf8]{inputenc}`.
- **Citations.** Match the template's backend (`natbib` vs `biblatex`+`biber`); never mix `\cite` / `\citep` / `\citet` styles across the document.
- **Cross-references.** `\cref{...}` / `\Cref{...}` only; never hand-write `Section~\ref{...}`.
- **Floats.** Always `[!htbp]`; in two-column docs use `figure*` / `table*` (only `[!t]` / `[!b]` accepted). Insert `\FloatBarrier` (placeins) or `\clearpage` to keep floats in their section.
- **Tables.** `booktabs` (`\toprule \midrule \bottomrule`) only; no vertical rules, no `\hline`. Numeric columns use `siunitx` `S[table-format=...]`; units in the header.
- **Equations.** Number central equations and `\label` them; multi-line uses `align`/`split`, never `eqnarray`.
- **Listings.** `breaklines=true`. Long listings move to an appendix.
- **Caption placement.** Above tables, below figures (community convention; follow the template if it differs).
- **References hygiene.** Every `\bibitem` is `\cite`'d at least once; resolve every `Citation 'x' undefined` and `LaTeX Warning: There were undefined references` in the `.log` before delivery.

## LaTeX Pitfalls

| Symptom | Fix |
|---|---|
| Floats drift far from text | `[!htbp]` + `\FloatBarrier`/`\clearpage` at section ends |
| Two-column doc, full-width float missing | Use `figure*`/`table*`; only `[!t]` or `[!b]` |
| Long table breaks ugly | `longtable`, or `scripts/longtable_to_tabular.lua` filter when converting from markdown |
| Unicode error under pdflatex | Switch to `tectonic`, or add `inputenc`+`fontenc` |
| `\hline` mixed with booktabs | Drop `\hline` entirely; use `\toprule/\midrule/\bottomrule` |
| `subfig` / `subcaption` clash | Use `subcaption` only |
| Citations style wrong | Match the template's expected backend; `latexmk -pdf` re-runs biber if needed |

## Build And Render Commands

**Tectonic** (default; auto-handles BibTeX and most cross-refs):

```bash
tectonic /path/to/main.tex
```

**latexmk** (use when biber, glossaries, or indexes are required):

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error /path/to/main.tex
```

**Render PDF pages to PNG** (visual QA):

```bash
python ~/.cursor/skills/write-report/scripts/validate_pdf.py \
  /path/to/report.pdf \
  --output-dir /path/to/qa_evidence/round<N>/page_images \
  --scale 2.0
```

**Markdown → LaTeX → PDF helper** (only for `iclr` / `cvpr` templates; otherwise write `.tex` directly):

```bash
python ~/.cursor/skills/write-report/scripts/build.py \
  --mode tex --template <iclr|cvpr> \
  --input content.md --figures ./figures --output report.pdf
```

## Toolchain

**Available**: tectonic, latexmk, bibtex, biber (optional), pypandoc, pypdfium2, Pillow, pypdf, pdfplumber, markitdown. Use `chktex` and `latexindent` only if present.

**Do not use**: HTML/CSS as a report source, weasyprint, Playwright, `pdflatex` / `xelatex` directly (use tectonic or latexmk), `soffice`, PPTX generation.
