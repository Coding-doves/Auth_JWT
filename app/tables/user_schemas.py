from app.config.database import Base

from  datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Boolean


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String, index=True)
    lastname = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hash_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    created_date = Column(DateTime, nullable=True, default=datetime.utcnow())
    updated_date = Column(DateTime, nullable=True, default=None, onupdate=datetime.utcnow())
    verified_date = Column(DateTime, nullable=True, default=None)

"""
class UserProfile(Base):
    __tablename__ = "user_profile"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String, index=True)
    lastname = Column(String, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hash_password = Column(String, nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow())
"""
