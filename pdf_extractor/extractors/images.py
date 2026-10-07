"""Extraction of images embedded in a PDF."""

import sys
from pathlib import Path

import pymupdf


def extract_images(doc: "pymupdf.Document", output_dir: Path) -> int:
    """
    Extract all images embedded in the PDF, preserving their original
    format and resolution (no recompression or rescaling).

    Saves them to <output_dir>/images/pageNNN_imgMM.ext

    Returns the number of images successfully extracted.
    """
    images_dir = output_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    total = 0
    for page_num in range(len(doc)):
        page = doc[page_num]
        images = page.get_images(full=True)

        for idx, img in enumerate(images, start=1):
            xref = img[0]
            try:
                image_data = doc.extract_image(xref)
            except Exception as e:
                print(
                    f"  [!] Could not extract an image on page "
                    f"{page_num + 1}: {e}",
                    file=sys.stderr,
                )
                continue

            extension = image_data["ext"]
            image_bytes = image_data["image"]

            filename = (
                f"page{page_num + 1:03d}_img{idx:02d}.{extension}"
            )
            image_path = images_dir / filename
            image_path.write_bytes(image_bytes)
            total += 1

    return total
