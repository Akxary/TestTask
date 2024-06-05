from fastapi import APIRouter
from routes.start_router import router as start_router
from routes.calc_router import router as calc_router
from routes.load_result_router import  router as load_result_router


router = APIRouter(prefix="/api", tags=["api"])
router.include_router(start_router)
router.include_router(calc_router)
router.include_router(load_result_router)