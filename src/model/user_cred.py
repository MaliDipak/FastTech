from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.model.declarative_base import Base


class UserCred(Base):
    __tablename__ = "user_cred"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    hash_password = Column(String, nullable=False)

    user = relationship("User", back_populates="credential")