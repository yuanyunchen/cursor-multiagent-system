---
name: webpage-content-extraction
description: Extract raw content (text + figures) from web pages. Fetches text via WebFetch, discovers and downloads images from raw HTML (WebFetch silently drops images). Falls back to Chrome headless PDF conversion for JS-rendered graphics, running the full PDF extraction pipeline on the rendered page. For document files (PDF, DOCX, PPTX), use file-content-extraction instead.
---

# Web Page Content Extraction

Extract COMPLETE content from a web page. Produce a `content.md` file that faithfully captures all text and figures, with figures placed inline at their original positions.

## Scope

This skill handles: **web pages (URLs).** For document files (PDF, DOCX, PPTX, images), use the `file-content-extraction` skill at `~/.cursor/skills/file-content-extraction/SKILL.md`.

This skill **extracts content only**. It does not:
- Reorganize, restructure, or rewrite content
- Remove "unimportant" sections
- Summarize or interpret meaning
- Delete intermediate files or clean up directories

Those tasks belong to the **file-extractor agent**, which invokes this skill as a first step, then organizes the extracted content.

## Input & Output

**Input:** A URL.

**Output:** Written to the specified output directory:
- `<output_dir>/content.md` — faithful extraction with:
  - Full text from the page
  - Inline figure references: `![description](figures/fig_{N}.png)`
  - Tables rendered as markdown tables
  - A Figure Index table at the end for quick reference
  - Extraction notes (if issues encountered)
- `<output_dir>/figures/` — downloaded figures, named `fig_{N}.png`

### Figure Naming Convention
- `fig_{N}.png` — sequential numbering matching order of appearance in page
- After download, filter out:
  - Small icons and emojis (below 200px on either dimension or below 80,000px² area)
  - Duplicate downloads (same URL appearing multiple times)

---

## Extraction Strategy

### Step 1 — Fetch text

Use `WebFetch` to get the page as markdown. This is the primary source for **text content**. WebFetch reads the full DOM, including content inside collapsed `<details>` elements, tabs, and accordions.

**Important:** `WebFetch` silently drops `<img>` tags during HTML-to-markdown conversion. Do NOT rely on it for image discovery — that is handled in Step 2.

### Step 2 — Discover and download images from raw HTML

Fetch the raw HTML separately and extract `<img>` sources:
```
curl -sL "<url>" | rg -o '<img[^>]+src="([^"]*)"' -r '$1' | sort -u > /tmp/img_urls.txt
```

For each image URL in the list:
1. Resolve relative URLs against the page's base URL (e.g., `/assets/fig.png` → `https://example.com/assets/fig.png`).
2. Download to `<output_dir>/figures/`:
```
curl -sL -o <output_dir>/figures/fig_{N}.png "<absolute_image_url>"
```
3. After downloading all, filter out small/decorative images:
   - Remove images below 200px on either dimension or below 80,000px² area.
   - Remove duplicate downloads (same URL appearing multiple times).
4. Name sequentially: `fig_1.png`, `fig_2.png`, etc.

If the `rg` command finds zero `<img>` tags but the text from Step 1 references figures (e.g., "the image below", "as shown in the figure"), the page likely uses JS-rendered graphics or CSS background images — proceed to the Fallback.

### Step 3 — Figure inspection

For every figure in `figures/`, use `Read` to view the image. Describe content, note what it illustrates, and map it back to the corresponding text section.

### Step 4 — Assemble content.md

Write `content.md` using the text from Step 1, inserting figure references (`![description](figures/fig_{N}.png)`) at the positions where the original page had images. Use the figure descriptions from Step 3 as alt text. Append a Figure Index table at the end.

---

## Fallback — PDF conversion

Use when Step 2 yields zero images on a page that references figures, or when the page uses JS-rendered charts (echarts, d3, chart.js, plotly, canvas-based graphics).

**Step F1 — Render page to PDF:**
```
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --print-to-pdf=<output_dir>/page.pdf \
  --no-pdf-header-footer "<url>"
```

**Step F2 — Run the full PDF extraction pipeline on `page.pdf`:**
Follow the `file-content-extraction` skill's PDF strategy (all three steps) on `page.pdf`:
1. `Read` the rendered PDF directly.
2. Run `python ~/.cursor/skills/file-content-extraction/extract_doc.py <output_dir>/page.pdf <output_dir>/pdf_extraction` to produce `content.md` + `figures/`.
3. Inspect each extracted figure with `Read`.

**Step F3 — Merge results:**
- **Text:** Use the text from WebFetch (Step 1) as the primary source — it preserves links, code blocks, and formatting better than PDF-extracted text. Only supplement with PDF-extracted text if WebFetch missed significant content.
- **Figures:** Merge figures from the PDF extraction into `<output_dir>/figures/`. Rename to continue the `fig_{N}` sequence. Deduplicate any figures that appear in both sources.

---

## Output Quality

The `content.md` produced by this skill is a **faithful extraction**, not a polished document:
- Text preserves the page's original structure and order.
- Figures are placed inline at the positions where they appeared on the page.
- The Figure Index table at the end provides a quick reference.
- No content is removed or summarized.

The **file-extractor agent** takes this raw extraction and produces the final structured, organized output.

---

## Rules

1. **Completeness is paramount.** Missing content is failure. When in doubt, include it.
2. **Never trust WebFetch for images.** Always run the raw HTML image discovery (Step 2) regardless of what WebFetch returns.
3. **Text from WebFetch, figures from raw HTML.** These are separate pipelines. The PDF fallback supplements figures — it does not replace WebFetch text.
4. **Full PDF pipeline on fallback.** When the fallback is triggered, run the complete PDF extraction (Read + script + figure inspection), not just figure extraction.
5. **Cross-check.** After assembling content.md, verify that every figure referenced in the text has a corresponding file in `figures/`. Flag any gaps.
6. **Preserve source structure.** Do not reorganize content. Keep the page's original order.
7. **Flag uncertainty** rather than guessing.
