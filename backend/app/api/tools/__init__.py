from fastapi import APIRouter, Depends

from app.api.tools.pdf import router as pdf_router
from app.dependencies import get_current_user

router = APIRouter(dependencies=[Depends(get_current_user)])

router.include_router(pdf_router, prefix="/pdf", tags=["Tools: PDF"])
