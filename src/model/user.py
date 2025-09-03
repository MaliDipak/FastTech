from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.model.declarative_base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)

    # One-to-one relationship with UserCred
    credential = relationship("UserCred", back_populates="user", uselist=False)