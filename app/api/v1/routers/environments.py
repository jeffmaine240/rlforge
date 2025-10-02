# app/api/v1/routers/environment.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession as Session

from app.dependencies.permissions import require_admin, require_authenticated, require_superadmin
from app.models.user import User
from app.schemas.environment import EnvironmentCreate, EnvironmentStep, EnvironmentResponse
from app.services.environment import EnvironmentService
from app.db.session import get_db_session

env_router = APIRouter(prefix="/environments", tags=["Environments"])
env_service = EnvironmentService()


@env_router.post("", response_model=EnvironmentResponse, summary="Create a new environment")
async def create_environment(
    data: EnvironmentCreate,
    db: Session = Depends(get_db_session),
    user: User = Depends(require_admin)
):
    """
    Create a new environment.
    Only users with admin privileges can perform this action.
    """
    try:
        env = await env_service.create_environment(data.name, data.env_id, db, user)
        return env
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@env_router.post("/{name}/step", summary="Perform a step in the environment")
async def step_environment(
    name: str,
    step: EnvironmentStep,
    user: User = Depends(require_authenticated)
):
    """
    Perform a single step in the given environment.
    Any authenticated user can perform steps.
    """
    try:
        return await env_service.step_environment(name, step.action)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@env_router.post("/{name}/reset", summary="Reset an environment")
async def reset_environment(
    name: str,
    db: Session = Depends(get_db_session),
    user: User = Depends(require_admin)
):
    """
    Reset the environment to its initial state.
    Only admins can reset environments.
    """
    try:
        return await env_service.reset_environment(name, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@env_router.delete("/{name}", summary="Delete an environment")
async def delete_environment(
    name: str,
    db: Session = Depends(get_db_session),
    user: User = Depends(require_superadmin)
):
    """
    Permanently delete an environment.
    Only superadmins can perform this action.
    """
    try:
        await env_service.delete_environment(name, db)
        return {"message": f"Environment '{name}' deleted successfully."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
