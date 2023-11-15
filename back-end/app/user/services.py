from typing import Optional, List, Type, Any

from sqlalchemy import or_, select, and_, cast
from sqlalchemy.dialects.postgresql import UUID

from app.user.models import User
from app.user.schemas import LoginResponseSchema, UpdateUserRequestSchema
from core.db import Transactional, session
"""from core.exceptions import (
    PasswordDoesNotMatchException,
    DuplicateEmailOrNicknameException,
    UserNotFoundException,
    CanSetRoleException
)"""
#from core.exceptions.user import CannotCreateExternalObjectException
from core.utils.token_helper import TokenHelper


class UserService:
    def __init__(self):
        ...

    
