from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.config import ALLOWED_IMAGE_TYPES, ALLOWED_PDF_TYPES
from app.services import pdf as pdf_service
from app.services.uploads import read_upload

router = APIRouter()


@router.post("/merge")
async def merge(files: list[UploadFile] = File(...)):
    if len(files) < 2:
        raise HTTPException(status_code=400, detail="Upload at least 2 PDF files")

    contents = [await read_upload(f, ALLOWED_PDF_TYPES) for f in files]

    try:
        path = pdf_service.merge_pdfs(contents)
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Failed to merge PDF files") from exc

    return FileResponse(path, media_type="application/pdf", filename="merged.pdf")


@router.post("/split")
async def split(
    file: UploadFile = File(...),
    start_page: int = Form(...),
    end_page: int = Form(...),
):
    if start_page < 1 or end_page < start_page:
        raise HTTPException(status_code=400, detail="Invalid page range")

    content = await read_upload(file, ALLOWED_PDF_TYPES)

    try:
        path = pdf_service.split_pdf(content, start_page, end_page)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Failed to split PDF file") from exc

    return FileResponse(path, media_type="application/pdf", filename="split.pdf")


@router.post("/image-to-pdf")
async def image_to_pdf(files: list[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="Upload at least 1 image file")

    contents = [await read_upload(f, ALLOWED_IMAGE_TYPES) for f in files]

    try:
        path = pdf_service.images_to_pdf(contents)
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Failed to convert images to PDF") from exc

    return FileResponse(path, media_type="application/pdf", filename="images.pdf")
