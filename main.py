#!/usr/bin/env python3
"""
PDF content extractor (images and/or plain text).

Usage:
    python main.py -i file.pdf -o ./output
    python main.py -i file.pdf -o ./output --images
    python main.py -i file.pdf -o ./output --text
    python main.py                                      (interactive mode)
"""

import sys

import pymupdf

from pdf_extractor.cli import resolve_options, normalize_path
from pdf_extractor.validators import validate_input
from pdf_extractor.extractors import extract_images, extract_text


def main() -> None:
    options = resolve_options()

    input_path = normalize_path(options.input_path_str)
    output_path = normalize_path(options.output_path_str)

    error = validate_input(input_path)
    if error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)

    try:
        doc = pymupdf.open(input_path)
    except Exception as e:
        print(f"Error: could not open the PDF: {e}", file=sys.stderr)
        sys.exit(1)

    output_path.mkdir(parents=True, exist_ok=True)

    print(f"Processing: {input_path.name} ({len(doc)} pages)")
    print(f"Output folder: {output_path}\n")

    if options.extract_images:
        print("Extracting images...")
        count = extract_images(doc, output_path)
        print(f"  -> {count} image(s) extracted to: {output_path / 'images'}\n")

    if options.extract_text:
        print("Extracting text...")
        pages = extract_text(doc, output_path)
        print(f"  -> Text from {pages} page(s) saved to: {output_path / 'text.txt'}\n")

    doc.close()
    print("Done.")


if __name__ == "__main__":
    main()
