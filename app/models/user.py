from sqlalchemy import Boolean, Column, DateTime, Enum, String
from sqlalchemy.orm import relationship

from app.core.enums import UserRole
from app.models.base import BaseModel



class User(BaseModel):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=True)
    last_login_at = Column(DateTime, nullable=True)

    is_active = Column(Boolean, default=True, nullable=True)
    role = Column(Enum(UserRole), default=UserRole.user, nullable=False)

    environments = relationship("Environment", back_populates="owner")

    def __repr__(self):
        return (
            f"<User(id={self.id}, email={self.email}, role={self.role}, "
            f"last_login_at={self.last_login_at})>"
        )

    @property
    def is_superadmin(self) -> bool:
        return self.role == UserRole.superadmin

    @property
    def is_admin(self) -> bool:
        return self.role in [UserRole.admin, UserRole.superadmin]
