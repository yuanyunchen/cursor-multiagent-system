---
name: file-content-extraction
description: Extract raw content (text + figures) from document files (PDF, DOCX, PPTX, images). Produces a faithful content.md with inline figure references and a figures/ directory. Does NOT reorganize, summarize, or interpret — that is the file-extractor agent's job. Not needed for lightweight files (text, markdown, CSV) — those can be read natively. For web pages, use the webpage-content-extraction skill instead.
---

# File Content Extraction

Extract COMPLETE content from a document file. Produce a `content.md` file that faithfully captures all text and figures from the source, with figures placed inline at their original positions.

## Scope

This skill handles: **PDF, DOCX, PPTX, images.** For web pages (URLs), use the `webpage-content-extraction` skill at `~/.cursor/skills/webpage-content-extraction/SKILL.md`.

This skill **extracts content only**. It does not:
- Reorganize, restructure, or rewrite content
- Remove "unimportant" sections
- Summarize or interpret meaning
- Delete intermediate files or clean up directories

Those tasks belong to the **file-extractor agent**, which invokes this skill as a first step, then organizes the extracted content.

## Input & Output

**Input:** A file path (PDF, DOCX, PPTX, or image).

**Output:** Written to the specified output directory:
- `<output_dir>/content.md` — faithful extraction with:
  - Full text organized by page/slide boundaries
  - Inline figure references at their source positions: `![Page N figure — WxHpx](figures/p{N}_fig_{M}.png)`
  - Tables rendered as markdown tables
  - A Figure Index table at the end for quick reference
  - Extraction notes (if issues encountered)
- `<output_dir>/figures/` — extracted figures, named `p{page}_fig_{N}.png`

### Figure Naming Convention
- **PDF:** `p{page}_fig_{N}.png` — page number from the source PDF, N is the figure index within that page
- **DOCX/PPTX:** `fig_{N}.png` — sequential numbering (no page concept available from extraction)
- The extraction script automatically filters out:
  - Alpha masks (smask)
  - Small icons and emojis (below 200px on either dimension or below 80,000px² area)
  - Duplicate images (same embedded object reused across pages)

---

## Strategy by File Type

### PDF

**Step 1 — Native Read:**
Use the `Read` tool directly on the PDF. This provides:
- Immediate understanding of structure, length, and content type.
- Text that may be missed or reformatted by the extraction script.
- A baseline to compare against later extraction results.

**Step 2 — Script Extraction:**
```
python ~/.cursor/skills/file-content-extraction/extract_doc.py <input_path> <output_dir>
```
Produces `content.md` + `figures/p{page}_fig_{N}.png`.
Read `content.md` fully. Compare against Step 1 — note any differences.

**Step 3 — Figure Inspection:**
For every figure in `figures/`, use `Read` to view the image:
- Describe diagrams, charts, graphs, photos, layouts.
- Note spatial relationships, labels, legends, axes, annotations.
- Identify anything present visually but absent from text extraction.
- Use the figure name (`p{page}_fig_{N}.png`) to locate where in content.md this figure belongs.

**Cross-check:** Union of all three steps = final content. Include anything caught by any step. Flag discrepancies.

**Adaptive:** Pure-text PDFs (no figures extracted) → Step 1 may suffice. Visual-heavy PDFs → all three steps are essential.

---

### DOCX

1. Use `Read` directly on the file for initial understanding.
2. Run: `python ~/.cursor/skills/file-content-extraction/extract_doc.py <input_path> <output_dir>`
   - Extracts text (headings, paragraphs, lists, tables) via `python-docx`.
   - Extracts embedded images into `figures/` (filtered for meaningful content).
3. Read `content.md` fully. Compare against Step 1.
4. View each figure with `Read`. Describe what each figure shows.
5. Watch for: headers/footers, footnotes, tracked changes, text boxes, SmartArt, or equations that `python-docx` cannot extract.

---

### PPTX

1. Use `Read` directly on the file for initial understanding.
2. Run: `python ~/.cursor/skills/file-content-extraction/extract_doc.py <input_path> <output_dir>`
   - Extracts text (slide titles, body text, notes, tables) via `python-pptx`.
   - Extracts embedded images into `figures/` (filtered for meaningful content).
3. Read `content.md` fully. Compare against Step 1.
4. View each figure with `Read`. Describe what each figure shows.
5. Watch for: speaker notes, visual layouts flattened by extraction, SmartArt.

---

### Image

Use `Read` directly on the image. Describe:
- All visible text.
- Diagrams, charts, graphs: structure, labels, values, relationships.
- Layouts: spatial arrangement, sections, visual hierarchy.
- Handwritten content, annotations, watermarks.

For text-heavy images, also run the extraction script for better OCR.

---

## Output Quality

The `content.md` produced by this skill is a **faithful extraction**, not a polished document:
- Text is organized by page/slide boundaries (not by semantic topics).
- Figures are placed inline at the page where they appeared in the source.
- The Figure Index table at the end provides a quick reference with page, dimensions, and file path.
- No content is removed or summarized.

The **file-extractor agent** takes this raw extraction and produces the final structured, organized output.

---

## Rules

1. **Completeness is paramount.** Missing content is failure. When in doubt, include it.
2. **Be adaptive.** A 3-page text PDF requires different effort than a 50-page visual slide deck.
3. **Read first, extract second.** Always use `Read` on the file first. The script supplements.
4. **Cross-check.** Text extraction misses visuals. Visual inspection misses searchable text. Use both.
5. **Preserve source structure.** Keep page/slide boundaries. Do not reorganize.
6. **Minimize tokens, maximize information.** Compress formatting, not content.
7. **Flag uncertainty** rather than guessing.
