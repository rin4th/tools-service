from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.config import ALLOWED_AVATAR_TYPES, AVATAR_DIR, MAX_AVATAR_SIZE
from app.database import get_db
from app.dependencies import get_current_user
from app.models import User
from app.schemas import ChangePasswordRequest, UserOut
from app.security import hash_password, verify_password

router = APIRouter()


def _avatar_url(user: User) -> str | None:
    if not user.avatar_path:
        return None
    return f"/api/profile/avatar/{user.id}"


@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return UserOut(
        id=current_user.id,
        username=current_user.username,
        avatar_url=_avatar_url(current_user),
    )


@router.post("/avatar", response_model=UserOut)
async def change_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if file.content_type not in ALLOWED_AVATAR_TYPES:
        raise HTTPException(status_code=400, detail=f"Unsupported avatar type: {file.content_type}")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Avatar file is empty")
    if len(content) > MAX_AVATAR_SIZE:
        raise HTTPException(status_code=413, detail="Avatar file is too large")

    suffix = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/webp": ".webp",
    }[file.content_type]

    filename = f"user-{current_user.id}-{uuid4().hex}{suffix}"
    target = AVATAR_DIR / filename
    target.write_bytes(content)

    if current_user.avatar_path:
        old = AVATAR_DIR / current_user.avatar_path
        if old.exists() and old.is_file():
            old.unlink(missing_ok=True)

    current_user.avatar_path = filename
    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    return UserOut(
        id=current_user.id,
        username=current_user.username,
        avatar_url=_avatar_url(current_user),
    )


@router.get("/avatar/{user_id}")
def get_avatar(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None or not user.avatar_path:
        raise HTTPException(status_code=404, detail="Avatar not found")

    path = AVATAR_DIR / user.avatar_path
    if not path.is_file():
        raise HTTPException(status_code=404, detail="Avatar file missing")

    suffix = Path(user.avatar_path).suffix.lower()
    media_type = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
    }.get(suffix, "application/octet-stream")

    return FileResponse(path, media_type=media_type)


@router.post("/change-password", status_code=status.HTTP_204_NO_CONTENT)
def change_password(
    payload: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not verify_password(payload.current_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    if payload.new_password == payload.current_password:
        raise HTTPException(status_code=400, detail="New password must differ from the current one")

    current_user.password_hash = hash_password(payload.new_password)
    db.add(current_user)
    db.commit()
