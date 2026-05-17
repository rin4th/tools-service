from io import BytesIO
from pathlib import Path
from uuid import uuid4

import img2pdf
from pypdf import PdfReader, PdfWriter

from app.config import OUTPUT_DIR


def _output_path(prefix: str, suffix: str = ".pdf") -> Path:
    return OUTPUT_DIR / f"{prefix}-{uuid4().hex}{suffix}"


def merge_pdfs(pdf_contents: list[bytes]) -> Path:
    writer = PdfWriter()
    for content in pdf_contents:
        reader = PdfReader(BytesIO(content))
        for page in reader.pages:
            writer.add_page(page)

    path = _output_path("merged")
    with path.open("wb") as f:
        writer.write(f)
    return path


def split_pdf(pdf_content: bytes, start_page: int, end_page: int) -> Path:
    reader = PdfReader(BytesIO(pdf_content))
    total = len(reader.pages)

    if end_page > total:
        raise ValueError(f"Page range exceeds total pages ({total})")

    writer = PdfWriter()
    for i in range(start_page - 1, end_page):
        writer.add_page(reader.pages[i])

    path = _output_path("split")
    with path.open("wb") as f:
        writer.write(f)
    return path


def images_to_pdf(image_contents: list[bytes]) -> Path:
    path = _output_path("images")
    path.write_bytes(img2pdf.convert(image_contents))
    return path
