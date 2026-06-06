from aiogram import Router

from bot.handlers.start import router as start_router
from bot.handlers.study import router as study_router


def setup_routers() -> Router:
    root = Router()
    root.include_router(start_router)
    root.include_router(study_router)
    return root
