from fastapi import HTTPException, UploadFile

from app.config import MAX_FILE_SIZE


async def read_upload(file: UploadFile, allowed_types: set[str], max_size: int = MAX_FILE_SIZE) -> bytes:
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.content_type}")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")
    if len(content) > max_size:
        raise HTTPException(status_code=413, detail="Uploaded file is too large")

    return content
