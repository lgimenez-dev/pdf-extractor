"""Input and output path validation."""

from pathlib import Path


def validate_input(input_path: Path) -> str | None:
    """
    Check that the input path is an existing, valid PDF.

    Returns None if everything is OK, or an error message otherwise.
    """
    if not input_path.exists():
        return f"File not found: {input_path}"
    if not input_path.is_file():
        return f"Path is not a file: {input_path}"
    if input_path.suffix.lower() != ".pdf":
        return (
            f"Input file must have a .pdf extension "
            f"(got: {input_path.suffix or '(no extension)'})"
        )
    return None


def normalize_path(path_str: str) -> Path:
    """
    Convert a path string into an absolute, normalized Path,
    stripping stray quotes (common when pasting copied paths on Windows).
    """
    clean_path = path_str.strip().strip('"').strip("'")
    return Path(clean_path).expanduser().resolve()
