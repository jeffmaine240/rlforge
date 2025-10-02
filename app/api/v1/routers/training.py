# app/api/v1/routers/training.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.dependencies.permissions import require_admin, require_authenticated
from app.db.session import get_db_session
from app.services.training import TrainingManager
from app.models.environment import Environment
from app.models.training import TrainingSession

training_router = APIRouter(prefix="/training", tags=["training"])

training_manager = TrainingManager()


@training_router.post("/{env_name}/start")
async def start_training(
    env_name: str,
    max_steps: int | None = None,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(require_admin)
):
    try:
        await training_manager.start_training(env_name, db, max_steps)
        return {"message": f"Training started for '{env_name}'."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@training_router.post("/{env_name}/stop")
async def stop_training(
    env_name: str,
    user=Depends(require_admin),
    db: AsyncSession = Depends(get_db_session)
):
    result = await training_manager.stop_training(env_name, db)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@training_router.get("/{env_name}/status")
async def training_status(env_name: str, user=Depends(require_authenticated)):
    return {"env_name": env_name, "is_training": training_manager.is_training(env_name)}


@training_router.get("/{env_name}/history")
async def training_history(
    env_name: str,
    db: AsyncSession = Depends(get_db_session),
    user=Depends(require_authenticated)
):
    # First, ensure the environment exists
    result = await db.execute(select(Environment).filter_by(name=env_name))
    env_obj = result.scalar_one_or_none()
    if not env_obj:
        raise HTTPException(status_code=404, detail=f"Environment '{env_name}' not found.")

    # Query training sessions for that environment
    result = await db.execute(select(TrainingSession).filter_by(environment_id=env_obj.id))
    sessions = result.scalars().all()

    return {"environment": env_name, "training_sessions": sessions}
