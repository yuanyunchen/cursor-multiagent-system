#!/usr/bin/env python3
"""Render each page of a PDF to a numbered PNG for visual inspection."""

import argparse
import os
import sys

import pypdfium2 as pdfium
from PIL import Image


def render_pages(pdf_path: str, output_dir: str, scale: float = 2.0) -> list[str]:
    os.makedirs(output_dir, exist_ok=True)
    pdf = pdfium.PdfDocument(pdf_path)
    paths = []
    for i, page in enumerate(pdf):
        bitmap = page.render(scale=scale)
        img = bitmap.to_pil()
        out = os.path.join(output_dir, f"page_{i + 1:03d}.png")
        img.save(out, "PNG")
        paths.append(out)
    print(f"Rendered {len(paths)} pages to {output_dir}/")
    for p in paths:
        print(f"  {p}")
    return paths


def main():
    parser = argparse.ArgumentParser(description="Render PDF pages to PNGs")
    parser.add_argument("pdf", help="Path to input PDF")
    parser.add_argument("--output-dir", default="./page_images", help="Output directory")
    parser.add_argument("--scale", type=float, default=2.0, help="Render scale (default 2.0)")
    args = parser.parse_args()

    if not os.path.isfile(args.pdf):
        print(f"Error: {args.pdf} not found", file=sys.stderr)
        sys.exit(1)

    render_pages(args.pdf, args.output_dir, args.scale)


if __name__ == "__main__":
    main()
