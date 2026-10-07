"""Extraction of plain text from a PDF to a .txt file."""

from pathlib import Path

import pymupdf


def extract_text(doc: "pymupdf.Document", output_dir: Path) -> int:
    """
    Extract the text of each page of the PDF and save it to a single
    plain text file (<output_dir>/text.txt), separating pages with
    a blank line.

    Returns the number of pages processed.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    txt_path = output_dir / "text.txt"

    parts = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text().strip()
        parts.append(text)
        parts.append("\n")

    txt_path.write_text("\n".join(parts), encoding="utf-8")
    return len(doc)
