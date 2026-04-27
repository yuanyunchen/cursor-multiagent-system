#!/usr/bin/env python3
"""Unified build script: markdown + figures -> PDF via LaTeX.

Usage:
  python build.py --mode tex --template iclr --input content.md --figures ./figures --output report.pdf
  python build.py --mode tex --template cvpr --input content.md --figures ./figures --output report.pdf
"""

import argparse
import re
import sys
from pathlib import Path

import pypandoc

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = SKILL_DIR / "templates"


def ensure_figures(md_path: Path, figures_dir: Path) -> None:
    """Fail fast if any figures referenced in markdown are missing."""
    text = md_path.read_text(encoding="utf-8")
    missing = []
    for m in re.finditer(r"!\[[^\]]*\]\(([^)]+)\)", text):
        rel = m.group(1).split("#")[0].split("?")[0].strip()
        img_path = md_path.parent / rel
        if not img_path.exists():
            alt_path = figures_dir / Path(rel).name
            if not alt_path.exists():
                missing.append(rel)
    if missing:
        print("Error: missing figure assets:", file=sys.stderr)
        for rel in missing:
            print(f"  {rel}", file=sys.stderr)
        sys.exit(1)


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


def main():
    parser = argparse.ArgumentParser(description="Build PDF from markdown")
    parser.add_argument("--mode", required=True, choices=["tex"])
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

    build_tex(input_md, figures_dir, output_pdf, args.template)


if __name__ == "__main__":
    main()
