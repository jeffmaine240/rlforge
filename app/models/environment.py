from sqlalchemy import Boolean, Column, DateTime, String, JSON, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import BaseModel

class Environment(BaseModel):
    __tablename__ = "environments"

    name = Column(String, unique=True, index=True, nullable=False)
    env_id = Column(String, unique=True, index=True, nullable=False)
    state = Column(JSON, nullable=True)
    is_training = Column(Boolean, default=False)
    last_trained_at = Column(DateTime(timezone=True), nullable=True)

    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="environments")

    training_sessions = relationship("TrainingSession", back_populates="environment", cascade="all, delete-orphan")
    
    def __repr__(self):
        return (
            f"<Environment(id={self.id}, name={self.name}, env_id={self.env_id}, "
            f"is_training={self.is_training}, last_trained_at={self.last_trained_at}, "
            f"user_id={self.user_id})>"
        )