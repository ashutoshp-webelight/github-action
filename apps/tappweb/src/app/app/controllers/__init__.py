from fastapi import APIRouter

from app.app.controllers.account import router as account_router
from app.app.controllers.admin import router as admin_router
from app.app.controllers.auth import router as auth_router
from app.app.controllers.cms_pages import router as cms_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
router.include_router(account_router, prefix="/account", tags=["Account"])
router.include_router(admin_router, prefix="/admin", tags=["Admin"])
router.include_router(cms_router, prefix="/cms", tags=["CMS"])
