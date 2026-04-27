---
name: pdf-to-markdown
description: >
  Convert PDF files to Markdown using Docling. Use when JPop (or any user) wants to
  convert one or more PDF books, documents, or files into Markdown for use in a RAG
  pipeline, knowledge base, or plain reading copy. Triggers on phrases like "convert
  this PDF", "turn my PDFs into markdown", "extract text from PDF", "I have PDF books
  I want to convert", or any request to ingest PDFs into a pipeline.
---

# PDF to Markdown (Docling)

Convert PDFs → clean Markdown using Docling. Good structure fidelity, strong table
handling, MIT license. CPU works; GPU is ~6x faster.

## Quickstart

```bash
# Single file
python3 skills/pdf-to-markdown/scripts/convert.py input.pdf [output.md]

# Whole folder (outputs to <folder>/markdown/ by default)
python3 skills/pdf-to-markdown/scripts/convert.py /path/to/books/ [/path/to/output/]
```

Outputs `.md` files next to inputs (single file) or in a `markdown/` subfolder (directory mode).

## Prerequisites

Docling must be installed:

```bash
pip install docling --break-system-packages
```

First run downloads OCR model weights (~15 MB) automatically. Subsequent runs are instant.

## When to Use Alternatives

| Situation | Use instead |
|-----------|-------------|
| Scientific PDFs with equations/LaTeX | Nougat (`pip install nougat-ocr`) |
| Need highest possible RAG structure fidelity | MinerU (`pip install mineru`) |
| Multi-format (Word, Excel, images too) | MarkItDown (`pip install markitdown`) |
| Scanned/image-only PDFs with poor quality | Zerox OCR (VLM-based, needs API key) |
| Table extraction only → CSV/pandas | Camelot or PDFPlumber |

## Notes

- Output goes next to the input file by default; specify a second arg to override.
- Docling is verbose on first run (model downloads). Normal.
- No GPU needed but install `torch` with CUDA for ~6x speedup on large batches.
- Full tool landscape: `knowledge/topics/pdf-to-markdown.md`
