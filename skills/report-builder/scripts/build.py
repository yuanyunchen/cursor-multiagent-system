#!/usr/bin/env python3
"""Unified build script: md + figures -> PDF via LaTeX or HTML.

Usage:
  python build.py --mode tex --template iclr --input content.md --figures ./figures --output report.pdf
  python build.py --mode tex --template cvpr --input content.md --figures ./figures --output report.pdf
  python build.py --mode html --input content.md --figures ./figures --output report.pdf
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

import pypandoc
from PIL import Image as PILImage, ImageDraw, ImageFont

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = SKILL_DIR / "templates"
STYLES_DIR = SKILL_DIR / "styles"

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def make_placeholder(path: Path, title: str) -> None:
    """Generate a placeholder PNG for a missing figure."""
    path.parent.mkdir(parents=True, exist_ok=True)
    width, height = 1800, 1080
    img = PILImage.new("RGB", (width, height), color=(247, 249, 252))
    draw = ImageDraw.Draw(img)
    border = (76, 102, 128)
    text_c = (47, 67, 88)
    draw.rectangle([(40, 40), (width - 40, height - 40)], outline=border, width=6)
    try:
        font_main = ImageFont.truetype("Arial.ttf", 52)
        font_sub = ImageFont.truetype("Arial.ttf", 38)
    except OSError:
        font_main = font_sub = ImageFont.load_default()
    msg = "Figure asset missing"
    bbox = draw.textbbox((0, 0), msg, font=font_main)
    draw.text(((width - bbox[2]) / 2, height / 2 - 40), msg, fill=text_c, font=font_main)
    bbox2 = draw.textbbox((0, 0), title, font=font_sub)
    draw.text(((width - bbox2[2]) / 2, height / 2 + 40), title, fill=text_c, font=font_sub)
    img.save(path, format="PNG")


def ensure_figures(md_path: Path, figures_dir: Path) -> None:
    """Create placeholder PNGs for any figures referenced in md but missing on disk."""
    text = md_path.read_text(encoding="utf-8")
    for m in re.finditer(r"!\[[^\]]*\]\(([^)]+)\)", text):
        rel = m.group(1).split("#")[0].split("?")[0].strip()
        img_path = md_path.parent / rel
        if not img_path.exists():
            alt_path = figures_dir / Path(rel).name
            if not alt_path.exists():
                make_placeholder(img_path, Path(rel).name)


def resolve_image_paths_for_html(md_text: str, figures_dir: Path) -> str:
    """Replace relative image paths with absolute file:// URLs for Chrome."""
    def replace_img(match):
        alt = match.group(1)
        rel = match.group(2).strip()
        abs_path = (figures_dir / Path(rel).name).resolve()
        if not abs_path.exists():
            candidate = (figures_dir.parent / rel).resolve()
            if candidate.exists():
                abs_path = candidate
        return f"![{alt}](file://{abs_path})"
    return re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", replace_img, md_text)


def build_tex(input_md: Path, figures_dir: Path, output_pdf: Path, template: str) -> Path:
    """Build PDF via LaTeX (pypandoc + tectonic). Returns path to saved .tex."""
    ensure_figures(input_md, figures_dir)

    sty_file = TEMPLATES_DIR / template / f"{'iclr2025_conference' if template == 'iclr' else 'cvpr'}.sty"
    if not sty_file.exists():
        print(f"Error: template {sty_file} not found", file=sys.stderr)
        sys.exit(1)

    tex_output = output_pdf.with_suffix(".tex")

    extra_args = [
        "--from=markdown+pipe_tables+fenced_code_blocks+implicit_figures+tex_math_dollars",
        "--standalone",
        f"--include-in-header={sty_file}",
        f"--resource-path={figures_dir}:{input_md.parent}",
        "--variable=papersize:letter",
        "--variable=colorlinks:true",
        "--variable=linkcolor:blue",
        "--variable=urlcolor:blue",
    ]

    if template == "cvpr":
        extra_args += ["--variable=classoption:twocolumn", "--variable=fontsize:10pt"]
        lua_filter = SKILL_DIR / "scripts" / "longtable_to_tabular.lua"
        if lua_filter.exists():
            extra_args.append(f"--lua-filter={lua_filter}")
    else:
        extra_args += ["--variable=fontsize:11pt"]

    tex_content = pypandoc.convert_file(
        str(input_md), to="latex", extra_args=extra_args
    )
    tex_output.write_text(tex_content, encoding="utf-8")
    print(f"Saved intermediate .tex: {tex_output}")

    pdf_args = extra_args + [f"--pdf-engine=tectonic"]
    pypandoc.convert_file(
        str(input_md), to="pdf", outputfile=str(output_pdf), extra_args=pdf_args
    )
    print(f"Built PDF: {output_pdf}")
    return tex_output


def build_html(input_md: Path, figures_dir: Path, output_pdf: Path) -> Path:
    """Build PDF via HTML (pypandoc -> jinja2 template -> Chrome headless). Returns path to saved .html."""
    import jinja2

    ensure_figures(input_md, figures_dir)

    template_file = STYLES_DIR / "blue-clean.html"
    if not template_file.exists():
        print(f"Error: HTML template {template_file} not found", file=sys.stderr)
        sys.exit(1)

    md_text = input_md.read_text(encoding="utf-8")
    md_text = resolve_image_paths_for_html(md_text, figures_dir)

    tmp_md = input_md.parent / "_tmp_resolved.md"
    tmp_md.write_text(md_text, encoding="utf-8")

    html_body = pypandoc.convert_file(
        str(tmp_md), to="html5",
        extra_args=["--from=markdown+pipe_tables+fenced_code_blocks+implicit_figures+tex_math_dollars"]
    )
    tmp_md.unlink(missing_ok=True)

    tmpl_text = template_file.read_text(encoding="utf-8")
    env = jinja2.Environment(loader=jinja2.BaseLoader(), autoescape=False)
    tmpl = env.from_string(tmpl_text)
    full_html = tmpl.render(content=html_body)

    html_output = output_pdf.with_suffix(".html")
    html_output.write_text(full_html, encoding="utf-8")
    print(f"Saved intermediate .html: {html_output}")

    cmd = [
        CHROME,
        "--headless",
        "--disable-gpu",
        f"--print-to-pdf={output_pdf}",
        "--no-pdf-header-footer",
        "--run-all-compositor-stages-before-draw",
        f"file://{html_output.resolve()}",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Chrome error: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    print(f"Built PDF: {output_pdf}")
    return html_output


def main():
    parser = argparse.ArgumentParser(description="Build PDF from markdown")
    parser.add_argument("--mode", required=True, choices=["tex", "html"])
    parser.add_argument("--template", choices=["iclr", "cvpr"], default="iclr",
                        help="LaTeX template (only for --mode tex)")
    parser.add_argument("--input", required=True, help="Path to content.md")
    parser.add_argument("--figures", required=True, help="Path to figures directory")
    parser.add_argument("--output", required=True, help="Output PDF path")
    args = parser.parse_args()

    input_md = Path(args.input).resolve()
    figures_dir = Path(args.figures).resolve()
    output_pdf = Path(args.output).resolve()

    if not input_md.is_file():
        print(f"Error: {input_md} not found", file=sys.stderr)
        sys.exit(1)

    output_pdf.parent.mkdir(parents=True, exist_ok=True)

    if args.mode == "tex":
        build_tex(input_md, figures_dir, output_pdf, args.template)
    else:
        build_html(input_md, figures_dir, output_pdf)


if __name__ == "__main__":
    main()
