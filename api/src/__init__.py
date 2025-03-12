from fastapi import APIRouter

from api.src.demo_auth.views import router as auth_router
from api.src.auth.endpoints import router as jwt_router

router = APIRouter()
# router.include_router(router=auth_router)
router.include_router(router=jwt_router)
