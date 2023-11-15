import uuid

from sqlalchemy import Column, Unicode, BigInteger, Boolean
from sqlalchemy.dialects.postgresql import UUID

from core.db import Base
from core.db.mixins import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    first_name = Column(Unicode(255), nullable=True)
    last_name = Column(Unicode(255), nullable=True)
    email = Column(Unicode(255), nullable=False, unique=True)
    nickname = Column(Unicode(255), nullable=False, unique=False)
    password = Column(Unicode(255), nullable=False)
    avatar = Column(Unicode(255), nullable=True)
    is_admin = Column(Boolean, default=False)
    role = Column(BigInteger)
