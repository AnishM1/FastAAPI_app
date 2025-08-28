from fastapi import APIRouter
from app import auth, api, chat


router = APIRouter()
router.include_router(auth.router)
router.include_router(api.router)
router.include_router(chat.router)

