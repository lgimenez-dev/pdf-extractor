"""Command-line interface: arguments and interactive mode."""

import argparse
from dataclasses import dataclass

from .validators import normalize_path


@dataclass
class Options:
    """Resolved options the program will run with."""
    input_path_str: str
    output_path_str: str
    extract_images: bool
    extract_text: bool


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pdf-extractor",
        description="Extract images and/or plain text from a PDF file.",
    )
    parser.add_argument(
        "-i", "--input",
        type=str,
        help="Path to the input PDF file.",
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="./output",
        help="Output folder (default: ./output).",
    )
    parser.add_argument(
        "--images",
        action="store_true",
        help="Extract images only.",
    )
    parser.add_argument(
        "--text",
        action="store_true",
        help="Extract plain text only (to a .txt file).",
    )
    return parser


def prompt_paths_interactive() -> tuple[str, str]:
    """Interactive fallback when no command-line arguments are given."""
    input_path_str = input("PDF path: ").strip()

    output_path_str = input(
        "Output folder (press Enter to use ./output): "
    ).strip()
    if not output_path_str:
        output_path_str = "./output"

    return input_path_str, output_path_str


def resolve_options(argv: list[str] | None = None) -> Options:
    """
    Parse the command-line arguments. If --input was not given, fall back
    to interactive mode and ask for the paths from the keyboard.
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    input_path_str = args.input
    output_path_str = args.output

    if not input_path_str:
        input_path_str, output_path_str = prompt_paths_interactive()

    # If no flag is specified, extract both by default
    no_flags = not (args.images or args.text)

    return Options(
        input_path_str=input_path_str,
        output_path_str=output_path_str,
        extract_images=args.images or no_flags,
        extract_text=args.text or no_flags,
    )


__all__ = ["Options", "resolve_options", "normalize_path"]
