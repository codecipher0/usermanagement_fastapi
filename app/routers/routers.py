from fastapi import APIRouter
from . import users, comments

router = APIRouter()

router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(comments.router, prefix="/comments", tags=["users"])