import os
import io
import tempfile
from pathlib import Path
from typing import Union, BinaryIO, Optional
from pdf2docx import Converter
import pikepdf


def convert_pdf_to_docx(
    input_pdf: Union[str, Path, bytes, BinaryIO],
    output_docx: Optional[Union[str, Path]] = None,
) -> Union[bytes, Path]:
    """
    Convert a PDF file to editable Microsoft Word DOCX format.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_pdf = os.path.join(temp_dir, "input.pdf")
        temp_docx = os.path.join(temp_dir, "output.docx")

        if isinstance(input_pdf, (str, Path)):
            with open(input_pdf, "rb") as f:
                content = f.read()
        elif isinstance(input_pdf, bytes):
            content = input_pdf
        else:
            content = input_pdf.read()

        with open(temp_pdf, "wb") as f:
            f.write(content)

        # Sanitize with pikepdf to repair syntax errors
        clean_pdf = os.path.join(temp_dir, "clean.pdf")
        try:
            with pikepdf.open(temp_pdf) as p:
                p.save(clean_pdf)
            src_pdf = clean_pdf
        except Exception:
            src_pdf = temp_pdf

        cv = Converter(src_pdf)
        cv.convert(temp_docx, start=0, end=None)
        cv.close()

        if output_docx is None:
            with open(temp_docx, "rb") as f:
                return f.read()

        out_path = Path(output_docx)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(temp_docx, "rb") as f_in, open(out_path, "wb") as f_out:
            f_out.write(f_in.read())
        return out_path
