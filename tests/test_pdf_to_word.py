import pytest
from pathlib import Path
import pikepdf
from pdfjin_pdf_to_word.core import convert_pdf_to_docx


def test_pdf_to_docx(tmp_path: Path):
    pdf_path = tmp_path / "test.pdf"
    docx_path = tmp_path / "test.docx"

    pdf = pikepdf.new()
    pdf.add_blank_page()
    pdf.save(str(pdf_path))

    res = convert_pdf_to_docx(pdf_path, output_docx=docx_path)
    assert res == docx_path
    assert docx_path.exists()
