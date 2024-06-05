from fastapi import APIRouter
from routes.start_router import router as start_router


router = APIRouter(prefix="/api", tags=["api"])
router.include_router(start_router)