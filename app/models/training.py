from sqlalchemy import Column, String, DateTime, JSON, ForeignKey, Integer, Float, func
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class TrainingSession(BaseModel):
    __tablename__ = "training_sessions"

    environment_id = Column(String, ForeignKey("environments.id"), nullable=False)
    started_at = Column(DateTime(timezone=True), nullable=False)
    ended_at   = Column(DateTime(timezone=True), nullable=True)

    observations = Column(JSON, nullable=True)
    rewards = Column(JSON, nullable=True)
    steps = Column(Integer, nullable=True)

    total_reward = Column(Float, nullable=True)

    environment = relationship("Environment", back_populates="training_sessions")

    def __repr__(self):
        return f"<TrainingSession(id={self.id}, env_id={self.environment_id}, started_at={self.started_at})>"
