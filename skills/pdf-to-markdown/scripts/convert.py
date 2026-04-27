#!/usr/bin/env python3
"""
PDF → Markdown conversion script using Docling.
Usage:
  python3 convert.py input.pdf [output.md]
  python3 convert.py /path/to/books/ [/path/to/output/]
"""

import sys
import os
from pathlib import Path


def convert_file(input_path: Path, output_path: Path) -> bool:
    """Convert a single PDF to Markdown. Returns True on success."""
    try:
        from docling.document_converter import DocumentConverter
    except ImportError:
        print("ERROR: docling not installed. Run: pip install docling", file=sys.stderr)
        sys.exit(1)

    print(f"Converting: {input_path.name} ...", end=" ", flush=True)
    try:
        converter = DocumentConverter()
        result = converter.convert(str(input_path))
        markdown = result.document.export_to_markdown()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(markdown, encoding="utf-8")
        print(f"→ {output_path}")
        return True
    except Exception as e:
        print(f"FAILED: {e}", file=sys.stderr)
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: convert.py <input.pdf|input_dir/> [output.md|output_dir/]")
        sys.exit(1)

    input_path = Path(sys.argv[1]).expanduser().resolve()

    if not input_path.exists():
        print(f"ERROR: Input not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    # --- Directory mode ---
    if input_path.is_dir():
        pdfs = sorted(input_path.glob("*.pdf"))
        if not pdfs:
            print(f"No PDFs found in {input_path}", file=sys.stderr)
            sys.exit(1)

        output_dir = Path(sys.argv[2]).expanduser().resolve() if len(sys.argv) > 2 else input_path / "markdown"
        print(f"Found {len(pdfs)} PDF(s) → {output_dir}\n")

        ok, fail = 0, 0
        for pdf in pdfs:
            out = output_dir / (pdf.stem + ".md")
            if convert_file(pdf, out):
                ok += 1
            else:
                fail += 1

        print(f"\nDone: {ok} converted, {fail} failed.")
        if fail:
            sys.exit(1)

    # --- Single file mode ---
    else:
        if not input_path.suffix.lower() == ".pdf":
            print(f"WARNING: input doesn't look like a PDF: {input_path.name}")

        if len(sys.argv) > 2:
            output_path = Path(sys.argv[2]).expanduser().resolve()
        else:
            output_path = input_path.with_suffix(".md")

        if not convert_file(input_path, output_path):
            sys.exit(1)


if __name__ == "__main__":
    main()
