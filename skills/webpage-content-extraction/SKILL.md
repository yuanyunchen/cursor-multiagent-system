---
name: webpage-content-extraction
description: Extract complete content (text + figures) from a web page URL. Produces a faithful content.md plus a figures/ directory. Use whenever a URL is the input — articles, blog posts, documentation pages, tutorials, papers rendered as HTML, anything where you want the page parsed for downstream use. Honors a `no_image` directive from the caller — when set, runs a fast text-only path via parallel-cli; default path includes full image discovery and Chrome PDF fallback for JS-rendered graphics. Do NOT use for local files (use file-content-extraction).
---

# Web Page Content Extraction

Extract the content of a web page into `content.md` (+ `figures/` when figures are wanted). The skill runs in one of two modes determined by the caller's `<parameters>` block.

## Modes

| Mode | Pipeline | Output | Use when |
|---|---|---|---|
| **Default** (`no_image: false`) | WebFetch text + raw HTML image discovery + Chrome PDF fallback | `content.md` with inline figure refs + `figures/` + Figure Index | figures matter (charts, diagrams, screenshots are part of the meaning) |
| **Text-only** (`no_image: true`) | `parallel-cli extract --full-content --no-excerpts` | `content.md` only | downstream just needs text (RAG, search index, summarization, report compilation) |

The text-only path is roughly an order of magnitude faster and produces equivalent text quality on most pages — including PDF URLs (`parallel-cli` handles those too).

## Output

Written to `<output_dir>`. Which files appear depends on the mode (see Modes table above). Conventions:

- `content.md` — page text in source order; in default mode, inline `![description](figures/fig_{N}.png)` references at original image positions plus a Figure Index table at the end; Extraction notes when something was unresolved.
- `figures/` (default mode only) — sequential `fig_1.png`, `fig_2.png`, … filtered to remove icons/decoration (below 200px on either side or 80,000 px² in area) and deduplicated by source URL.

## `no_image: true` — text-only path

```
parallel-cli extract "<url>" --full-content --no-excerpts --json -o <output_dir>/raw.json
```

Then write `results[0].full_content` from `raw.json` as `<output_dir>/content.md` and delete `raw.json`. That's the entire pipeline in this mode — no further steps.

If `parallel-cli` is not installed, the command will fail with "command not found". Stop and tell the user to run `/parallel-setup`. Do not silently fall back to WebFetch — text-only callers chose this path for speed.

## Default mode — full pipeline

Text and figures come from **separate** sources because no single tool reliably gives both.

### 1. Text — `WebFetch`

`WebFetch` reads the full DOM (including content inside collapsed `<details>`, tabs, accordions) and returns clean markdown. Primary text source.

It does **not** return images — silently. Do not rely on it for figure discovery.

### 2. Figures — raw HTML

```
curl -sL "<url>" | rg -o '<img[^>]+src="([^"]*)"' -r '$1' | sort -u > /tmp/img_urls.txt
```

For each URL, resolve relative paths against the page base, then download:

```
curl -sL -o <output_dir>/figures/fig_{N}.png "<absolute_image_url>"
```

After download, filter by size and deduplicate. Number sequentially in order of appearance on the page.

If `<img>` count is zero but the text references figures ("the chart below", "as shown"), the page likely renders graphics in JS or uses CSS backgrounds — proceed to the Chrome fallback below.

### 3. Figure inspection

`Read` every file in `figures/`. Describe what each shows and confirm it matches the surrounding text. Use those descriptions as alt text in the inline references.

### 4. Assemble `content.md`

Use Step 1's text as the body. Insert `![description](figures/fig_{N}.png)` at the positions where the original page had `<img>` tags. Append a Figure Index table. Add an Extraction notes section if anything was unresolved.

### Chrome PDF fallback (default mode only)

Use when Step 2 yields zero figures on a page that clearly references them, or when graphics are JS-rendered (echarts, d3, chart.js, plotly, canvas).

```
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --print-to-pdf=<output_dir>/page.pdf \
  --no-pdf-header-footer "<url>"
```

Then run `extract_doc.py` from `file-content-extraction` on `page.pdf` (without `--no-image`), inspect each extracted figure with `Read`, and merge:
- **Text** stays from `WebFetch` — it preserves links, code blocks, formatting better than PDF-extracted text.
- **Figures** from the PDF run are renamed into the `fig_{N}` sequence and merged into `<output_dir>/figures/`. Deduplicate against any figures already there.
- Delete `page.pdf` and the PDF run's intermediate dir before returning.

## Rules

1. **Pick the mode from `<parameters>`, never guess.** Default to `no_image: false` only if the parameter is absent. Switching modes mid-run produces inconsistent output structure.

2. **Never trust `WebFetch` for images.** In default mode, always run the raw-HTML discovery regardless of what `WebFetch` returns. This is the failure this skill exists to prevent.

3. **Text and figures are separate pipelines (default mode).** The Chrome fallback supplements figures only — it does not replace `WebFetch` text. Mixing the two text sources produces inconsistent formatting.

4. **Verify every reference resolves (default mode).** After assembly, every `![…](figures/fig_N.png)` in `content.md` must point at a real file in `figures/`. Flag any gaps in Extraction notes rather than silently dropping the reference.

5. **No half-states across modes.** A stray `figures/` dir, an `![…]` line pointing at a missing file, or a Figure Index in `no_image` mode all break downstream consumers silently. Whichever mode runs, its contract holds end-to-end.

6. **Preserve source order.** Do not reorganize content into topical sections — that is the calling agent's job.

7. **Flag uncertainty.** If text mentions a figure that no extraction step recovered, say so in Extraction notes. Better to flag than to hide.
