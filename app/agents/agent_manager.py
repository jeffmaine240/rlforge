import os
import pickle
from typing import Optional
from app.agents.q_agent import QAgent

MODEL_DIR = "agents/models"

os.makedirs(MODEL_DIR, exist_ok=True)

class AgentManager:
    @staticmethod
    def get_model_path(env_name: str) -> str:
        return os.path.join(MODEL_DIR, f"{env_name}_agent.pkl")

    @staticmethod
    def load(env_name: str) -> Optional[QAgent]:
        path = AgentManager.get_model_path(env_name)
        if os.path.exists(path):
            with open(path, "rb") as f:
                return pickle.load(f)
        return None

    @staticmethod
    def save(env_name: str, agent: QAgent):
        path = AgentManager.get_model_path(env_name)
        with open(path, "wb") as f:
            pickle.dump(agent, f)
