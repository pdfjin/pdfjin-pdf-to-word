import sys
import argparse
from pathlib import Path
try:
    from .core import convert_pdf_to_docx
    from . import __version__
except (ImportError, ValueError):
    from pdfjin_pdf_to_word.core import convert_pdf_to_docx
    from pdfjin_pdf_to_word import __version__


def main():
    parser = argparse.ArgumentParser(
        prog="pdfjin-pdf-to-word",
        description="Convert PDF documents into editable Word (.docx) documents.",
        epilog="Online web version available at https://pdfjin.com/pages/pdf-to-word.html",
    )
    parser.add_argument("input", metavar="INPUT_PDF", help="Path to the PDF file")
    parser.add_argument("-o", "--output", required=True, metavar="OUTPUT_DOCX", help="Path for output .docx file")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")

    args = parser.parse_args()

    try:
        out = convert_pdf_to_docx(args.input, output_docx=args.output)
        print(f"✨ Successfully converted -> {out}")
    except Exception as e:
        print(f"❌ Conversion failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
