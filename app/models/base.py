from sqlalchemy import Column, String, DateTime, Boolean, func
from datetime import datetime, timezone
from app.db.session import Base
import uuid

from app.utils.time import utcnow



class BaseModel(Base):
    __abstract__ = True
    """
    Declarative base for ORM models.

    Acts as the root for all mapped classes and provides a shared metadata registry.
    """

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    
