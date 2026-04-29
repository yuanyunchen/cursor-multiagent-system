---
name: webpage-content-extraction
description: Extract complete content (text + figures) from a web page URL with full image discovery. Produces a faithful content.md plus a figures/ directory. Use whenever a URL is the input and figures matter — articles, blog posts, documentation pages, tutorials, papers rendered as HTML, anything where charts/diagrams/screenshots are part of the meaning. Do NOT use for text-only URL extraction — the caller (file-extractor) bypasses this skill and uses /parallel-web-extract directly for that, since it's faster and gets equivalent text. Do NOT use for local files (use file-content-extraction).
---

# Web Page Content Extraction

Extract the **full** content of a web page — text in source order plus every meaningful image — into `content.md` + `figures/`. This skill exists for one reason: `WebFetch` silently drops `<img>` tags, so the only way to get faithful figure coverage is a separate raw-HTML pipeline.

## When this skill runs vs. when it doesn't

The caller (typically `file-extractor`) decides:
- **Text-only / `no_image: true`** → caller invokes `/parallel-web-extract` directly, **does not enter this skill**. That path is faster and the text quality is comparable.
- **Full / default** → caller invokes this skill for the complete pipeline below.

Inside this skill, assume figures are wanted. There is no "no-image mode" here — that case is routed elsewhere.

## Output

Written to `<output_dir>`:
- `content.md` — page text in source order; inline figure references `![description](figures/fig_{N}.png)` at the positions where the original page had images; Figure Index table at the end; Extraction notes if anything was uncertain.
- `figures/` — downloaded images, sequential `fig_1.png`, `fig_2.png`, …  Filtered to remove icons/decoration (below 200px on either side or 80,000 px² in area) and deduplicated by source URL.

## Pipeline

Text and figures come from **separate** sources because no single tool reliably gives both.

### 1. Text — `WebFetch`

`WebFetch` reads the full DOM (including content inside collapsed `<details>`, tabs, accordions) and returns clean markdown. This is the primary source for text.

It does **not** return images — silently. Do not rely on it for figure discovery.

### 2. Figures — raw HTML

Pull the raw HTML and extract `<img>` sources:

```
curl -sL "<url>" | rg -o '<img[^>]+src="([^"]*)"' -r '$1' | sort -u > /tmp/img_urls.txt
```

For each URL, resolve relative paths against the page base, then download:

```
curl -sL -o <output_dir>/figures/fig_{N}.png "<absolute_image_url>"
```

After download, filter by size and deduplicate. Number sequentially in order of appearance on the page.

If `<img>` count is zero but the text references figures ("the chart below", "as shown"), the page likely renders graphics in JS or uses CSS backgrounds — proceed to the fallback.

### 3. Figure inspection

`Read` every file in `figures/`. For each, describe what it shows and confirm it matches the surrounding text. Use these descriptions as the alt text in the inline references.

### 4. Assemble `content.md`

Use Step 1's text as the body. Insert `![description](figures/fig_{N}.png)` at the positions where the original page had `<img>` tags. Append a Figure Index table at the end. Add an Extraction notes section for anything unresolved.

## Fallback — Chrome PDF rendering

Use when Step 2 yields zero figures on a page that clearly references them, or when graphics are JS-rendered (echarts, d3, chart.js, plotly, canvas).

```
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --print-to-pdf=<output_dir>/page.pdf \
  --no-pdf-header-footer "<url>"
```

Then run the **full** PDF pipeline from `file-content-extraction` on `page.pdf` — `Read` the rendered PDF, run `extract_doc.py`, inspect each extracted figure. Merge results:
- **Text** stays from `WebFetch` (Step 1) — it preserves links, code blocks, and formatting better than PDF-extracted text.
- **Figures** from the PDF extraction are renamed into the `fig_{N}` sequence and merged into `<output_dir>/figures/`. Deduplicate against any figures already there.

## Rules

1. **Never trust `WebFetch` for images.** Always run Step 2 regardless of what `WebFetch` returns. This is the failure this skill exists to prevent.

2. **Text and figures are separate pipelines.** The PDF fallback supplements figures only — it does not replace `WebFetch` text. Mixing the two text sources produces inconsistent formatting.

3. **Verify every reference resolves.** After assembly, every `![…](figures/fig_N.png)` in `content.md` must point at a real file in `figures/`. Flag any gaps in Extraction notes rather than silently dropping the reference.

4. **Preserve source order.** Do not reorganize content into topical sections — that is the calling agent's job.

5. **Flag uncertainty.** If text mentions a figure that no extraction step recovered, say so in Extraction notes. Better to flag than to hide.
