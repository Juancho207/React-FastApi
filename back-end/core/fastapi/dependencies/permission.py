from abc import ABC, abstractmethod
from typing import List

from fastapi import Request
from fastapi.openapi.models import APIKey, APIKeyIn
from fastapi.security.base import SecurityBase

from app.user.enums import UserRole
from app.user.services import UserService
from core.exceptions import CustomException, UnauthorizedException


class BasePermission(ABC):
    exception = CustomException

    @abstractmethod
    async def has_permission(self, request: Request) -> bool:
        pass


class IsAuthenticated(BasePermission):
    exception = UnauthorizedException

    async def has_permission(self, request: Request) -> bool:
        return request.user.id is not None


class IsAdmin(BasePermission):
    exception = UnauthorizedException

    async def has_permission(self, request: Request) -> bool:
        user_id = request.user.id
        if not user_id:
            return False
        role = await UserService().get_role(user_id=user_id)
        return role == UserRole.ADMIN.value


class IsVenue(BasePermission):
    exception = UnauthorizedException

    async def has_permission(self, request: Request) -> bool:
        user_id = request.user.id
        if not user_id:
            return False
        role = await UserService().get_role(user_id=user_id)

        return role == UserRole.VENUE.value


class IsArtist(BasePermission):
    exception = UnauthorizedException

    async def has_permission(self, request: Request) -> bool:
        user_id = request.user.id
        if not user_id:
            return False
        role = await UserService().get_role(user_id=user_id)

        return role == UserRole.ARTIST.value


class AllowAll(BasePermission):
    async def has_permission(self, request: Request) -> bool:
        return True


class PermissionDependency(SecurityBase):
    def __init__(self, permissions: List[type[BasePermission]]):
        self.permissions = permissions
        self.model: APIKey = APIKey(**{"in": APIKeyIn.header}, name="Authorization")
        self.scheme_name = self.__class__.__name__

    async def __call__(self, request: Request):
        has_permission = False

        for permission in self.permissions:
            cls = permission()
            if await cls.has_permission(request=request):
                has_permission = True
                break
        if not has_permission:
            raise UnauthorizedException
