import gymnasium as gym
from typing import Dict
from app.models.environment import Environment
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User


class EnvironmentService:
    
    def __init__(self):
        self.environments: Dict[str, gym.Env] = {}

    async def create_environment(
        self, name: str, env_id: str, db: AsyncSession, owner: User
    ):
        if name in self.environments:
            raise ValueError(f"Environment '{name}' already exists.")

        env = gym.make(env_id)
        self.environments[name] = env

        db_env = Environment(
            name=name,
            env_id=env_id,
            state=None,
            user_id=owner.id
        )
        db.add(db_env)
        await db.commit()
        await db.refresh(db_env)
        return db_env

    async def step_environment(self, name: str, action: int):
        env = self.environments.get(name)
        if not env:
            raise ValueError(f"Environment '{name}' not found.")
        
        if not getattr(env, "_has_reset", False):
            env.reset()

        observation, reward, terminated, truncated, info = env.step(action)
        return {
            "observation": observation.tolist() if hasattr(observation, "tolist") else observation,
            "reward": reward,
            "terminated": terminated,
            "truncated": truncated,
            "info": info
        }

    async def reset_environment(self, name: str, db: AsyncSession):
        env = self.environments.get(name)
        if not env:
            raise ValueError(f"Environment '{name}' not found.")

        observation, info = env.reset()

        result = await db.execute(select(Environment).filter(Environment.name == name))
        env_db = result.scalars().first()
        if env_db:
            env_db.state = observation.tolist() if hasattr(observation, "tolist") else observation
            await db.commit()

        return {
            "observation": observation.tolist() if hasattr(observation, "tolist") else observation,
            "info": info
        }

    async def delete_environment(self, name: str, db: AsyncSession):
        if name not in self.environments:
            raise ValueError(f"Environment '{name}' not found in memory.")

        del self.environments[name]

        result = await db.execute(select(Environment).filter(Environment.name == name))
        env_db = result.scalars().first()
        if env_db:
            await db.delete(env_db)
            await db.commit()
