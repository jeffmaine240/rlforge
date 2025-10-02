from pydantic import BaseModel
from typing import Any, Optional


class EnvironmentCreate(BaseModel):
    name: str
    env_id: str


class EnvironmentStep(BaseModel):
    action: int


class EnvironmentResponse(BaseModel):
    id: str
    name: str
    env_id: str
    state: Optional[Any]
