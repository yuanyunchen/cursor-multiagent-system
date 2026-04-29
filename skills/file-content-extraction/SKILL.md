---
name: file-content-extraction
description: Extract complete raw content (text + figures) from a local document file — PDF, DOCX, PPTX, or image. Produces a faithful content.md plus a figures/ directory. Use this skill whenever the user wants a document parsed, ingested, summarized, or fed to another agent — including phrases like "read this PDF", "what's in slides.pptx", "extract the report", "process this paper". Do NOT use for URLs (use webpage-content-extraction) or for already-machine-readable files like .py / .md / .csv (read them natively). Honors a `no_image` directive from the caller — when set, produces text-only output and skips figure work.
---

# File Content Extraction

Extract everything a document carries — every paragraph, table, figure — into a `content.md` you can hand to any downstream consumer. **Faithful reproduction is the contract**: nothing is reorganized, summarized, or judged "unimportant". That work belongs to the `file-extractor` agent that calls this skill.

## Modes

The caller's task envelope may include `no_image: true` in `<parameters>`. Default is `no_image: false`.

| Mode | Output | Skip |
|---|---|---|
| **Default** (`no_image: false`) | `content.md` + `figures/` with inline `![…](figures/…)` references and a Figure Index table | nothing |
| **Text-only** (`no_image: true`) | `content.md` only | figure extraction, figure inspection, figure references |

Why this exists: figure inspection is the slowest step, and many downstream consumers (e.g. report-writer compiling text, RAG indexing) only need text. Honoring the flag at this layer prevents wasted work.

## Output

Written to `<output_dir>` provided by the caller. Which files appear depends on the mode (see Modes table above). Conventions:

- `content.md` — text organized by source page/slide boundaries; tables as markdown; in default mode, inline figure references at source positions plus a Figure Index table at the end; Extraction notes section when something was uncertain.
- `figures/` (default mode only) — `p{page}_fig_{N}.png` (PDF) or `fig_{N}.png` (DOCX/PPTX). Filtered: figures below 200px on either side or 80,000 px² in area are dropped (decorative/icon noise); duplicates (same embedded object reused across pages) are deduplicated.

## Workflow

The pipeline is the same shape for PDF/DOCX/PPTX; only the front-loaded `Read` step varies in value.

### 1. Native Read (always)

Use the `Read` tool on the input file directly. This gives an immediate sense of structure, length, and content type, and surfaces text the script may miss (non-standard encodings, embedded objects, OCR'd glyphs). The script result is then cross-checked against this baseline.

For pure images, `Read` is the entire extraction — describe all visible text, diagrams, labels, layouts, annotations.

### 2. Script extraction

```
# default — text + figures
python ~/.cursor/skills/file-content-extraction/extract_doc.py <input_path> <output_dir>

# no_image — text only, ~14× faster (skips pdfimages decode + PIL filtering)
python ~/.cursor/skills/file-content-extraction/extract_doc.py <input_path> <output_dir> --no-image
```

Pick the invocation by the caller's `no_image` parameter. The script handles the difference internally: with `--no-image` it never creates `figures/`, never inserts `![…]` references, and never writes the Figure Index. No post-processing needed.

Read `content.md` fully. Compare against Step 1 — note discrepancies in the Extraction notes section.

### 3. Figure inspection — **default mode only**

Use `Read` on every file in `figures/`. For each, describe what it shows (chart axes, labels, layout, what it illustrates) and verify the description matches the surrounding text in `content.md`. The figure name maps to its location in the page layout — use it to confirm the inline reference is positioned correctly.

Skip this step entirely when `--no-image` was used in Step 2 — there is no `figures/` directory to inspect.

### Type-specific notes

- **PDF** — visual-heavy decks need all three steps; pure-text PDFs may be done after Step 1 alone.
- **DOCX** — `python-docx` cannot extract headers/footers, footnotes, tracked changes, text boxes, SmartArt, or equations. Flag what's missing in Extraction notes.
- **PPTX** — `python-pptx` flattens visual layouts and may miss SmartArt. Speaker notes are extracted.
- **Image** — Step 1 only; no script needed unless OCR'd text is dense (then run the script for OCR pass).

## Rules

1. **Completeness is the contract.** Missing content is failure. When in doubt, include it. Faithful reproduction over perceived relevance — the calling agent decides what's important, not this skill.

2. **Read first, extract second.** Native `Read` always runs before the script — the script's job is to supplement, not replace, that baseline. Skipping Step 1 routinely loses non-OCR'd text and embedded objects the script can't handle.

3. **Preserve source structure.** Keep page/slide boundaries intact. Do not merge sections, reorder, or impose a topical organization — the `file-extractor` agent owns reorganization.

4. **No half-states.** Either both modes' contracts hold or neither does. In default mode, every figure file in `figures/` must be referenced from `content.md` and vice versa; in `no_image` mode, no figure references and no `figures/` exist. A `![…]` line pointing at a missing file (or a stray `figures/` dir with no references) breaks downstream consumers silently.

5. **Flag uncertainty.** Add an Extraction notes section at the end of `content.md` for anything you suspect is missing or garbled (failed equation, broken table, unreadable scan). Better to flag than to hide.
