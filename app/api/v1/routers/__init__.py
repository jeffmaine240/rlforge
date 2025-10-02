from fastapi import APIRouter
from .environments import env_router
from .auth import auth_router
from .training import training_router


router = APIRouter(prefix="/v1")


router.include_router(env_router)
router.include_router(auth_router)
router.include_router(training_router)