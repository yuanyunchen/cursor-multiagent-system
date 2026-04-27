#!/usr/bin/env python3
"""Inspect the local write-report template cache."""

import argparse
import json
import sys
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = SKILL_DIR / "templates"
MANIFEST = TEMPLATES_DIR / "manifest.json"


def load_manifest() -> dict:
    if not MANIFEST.is_file():
        print(f"Error: manifest not found: {MANIFEST}", file=sys.stderr)
        sys.exit(1)
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Check write-report template cache")
    parser.add_argument("scenario", help="Template scenario, e.g. generic-professional, cvpr, iclr")
    args = parser.parse_args()

    manifest = load_manifest()
    matches = [t for t in manifest.get("templates", []) if t.get("scenario") == args.scenario]
    if not matches:
        print(f"missing\t{args.scenario}")
        sys.exit(2)

    entry = matches[0]
    template_dir = TEMPLATES_DIR / entry["template_dir"]
    status = "present" if template_dir.is_dir() else "missing"
    freshness = entry.get("freshness", "unknown")
    print(f"{status}\t{args.scenario}\t{freshness}\t{template_dir}")
    if status != "present":
        sys.exit(2)
    if freshness in {"stale", "check-latest"}:
        sys.exit(3)


if __name__ == "__main__":
    main()
