import asyncio
from typing import Dict, Optional

import gymnasium as gym
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.environment import Environment
from app.models.training import TrainingSession
from app.utils.json import make_json_safe
from app.utils.time import to_naive_utc, utcnow
from app.core.logging import get_logger
from app.agents.agent_manager import AgentManager
from app.agents.q_agent import QAgent
from app.db.session import database

logger = get_logger("[TrainingManager]")


class TrainingManager:
    def __init__(self):
        self.active_trainings: Dict[str, asyncio.Task] = {}

    async def start_training(self, env_name: str, db: AsyncSession, max_steps: int = None):
        if env_name in self.active_trainings:
            raise ValueError(f"Environment '{env_name}' is already training.")

        result = await db.execute(select(Environment).filter_by(name=env_name))
        env_obj = result.scalars().first()
        if not env_obj:
            raise ValueError(f"Environment '{env_name}' not found.")

        env = gym.make(env_obj.env_id)
        agent = AgentManager.load(env_name) or QAgent(state_size=env.observation_space.shape[0],
                                                       action_size=env.action_space.n)

        env_obj.is_training = True
        await db.commit()

        task = asyncio.create_task(self._train(env_name, env, agent, db, max_steps))
        self.active_trainings[env_name] = task

    async def _train(self, env_name, env, agent: QAgent, db: AsyncSession, max_steps: int = None):
        """
        Internal asynchronous training loop.
        Records all observations, rewards, steps, and updates environment metadata.
        Supports optional maximum steps limit.
        """
        observation, _ = env.reset()
        done = False
        steps = 0
        states = [observation]
        rewards = []
        started_at = utcnow()

        while not done:
            action = agent.choose_action(observation)
            next_obs, reward, terminated, truncated, _ = env.step(action)

            agent.learn(observation, action, reward, next_obs, terminated)
            observation = next_obs

            states.append(observation)
            rewards.append(reward)
            steps += 1

            done = terminated or truncated
            if max_steps and steps >= max_steps:
                done = True

            logger.info(f"[TRAIN] {env_name} Step={steps}, Reward={reward}, Done={done}")
            await asyncio.sleep(0)

        ended_at = utcnow()
        logger.info(f"[TRAIN] ended at: {ended_at}")
        async with database.get_session() as db:
            try:
                logger.info(f"[TRAIN][DB] Saving TrainingSession with {steps} steps, total reward={sum(rewards)}")

                result = await db.execute(select(Environment).filter_by(name=env_name))
                env_obj = result.scalars().first()
                env_obj.is_training = False
                env_obj.last_trained_at = make_json_safe(ended_at)
                env_obj.state = make_json_safe(states[-1]) if states else None

                session = TrainingSession(
                    environment_id=env_obj.id,
                    started_at=to_naive_utc(started_at),
                    ended_at=to_naive_utc(ended_at),
                    observations=make_json_safe(states),
                    rewards=make_json_safe(rewards),
                    steps=int(steps),
                    total_reward=float(sum(rewards))
                )


                db.add(session)
                logger.debug(f"[DB] Committing session with dirty={db.dirty}, new={db.new}")
                await db.commit()
            except Exception as e:
                logger.exception(f"[TRAIN][DB] Error saving TrainingSession: {e}")
                await db.rollback()

        AgentManager.save(env_name, agent)
        self.active_trainings.pop(env_name, None)

    def is_training(self, env_name: str) -> bool:
        return env_name in self.active_trainings


    async def stop_training(self, env_name: str, db: AsyncSession):
        """
        Stop training early for a given environment.
        Cancels the associated task and updates environment state.
        """
        task = self.active_trainings.get(env_name)
        if task:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                logger.info(f"Training task for '{env_name}' cancelled successfully.")
            # Mark environment as not training
            await db.execute(update(Environment).where(Environment.name == env_name)
                             .values(is_training=False))
            await db.commit()
            return {"message": f"Training stopped for '{env_name}'"}
        return {"error": f"No active training for '{env_name}'"}
