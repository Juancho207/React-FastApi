from starlette.requests import Request

from app.user.services import UserService


class AuthenticatedUserType:
    def __init__(self):
        pass

    async def __call__(self, request: Request):
        user = await UserService().get_user_by_id(request.user.id)
        return user.role


