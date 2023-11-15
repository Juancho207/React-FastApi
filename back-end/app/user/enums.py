from enum import Enum


class BaseEnum(Enum):
    pass

class UserEnum(BaseEnum):
    pass

class UserRole(BaseEnum):
    NOROLE = 0
    ADMIN = 1
