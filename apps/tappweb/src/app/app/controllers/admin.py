from typing import Annotated

from fastapi import APIRouter, status, Body, Depends

from app.app.models.user import UserModel
from app.app.schemas import AdminCreateUserRequest, LoginRequest, LoginUserResponse, UserResponse, AdminUserResponse
from app.app.services import AdminService
from core.auth import HasPermission
from core.types import RoleType

router = APIRouter()


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=LoginUserResponse,
    response_description="",
    name="Login",
    description="",
)
async def admin_login(
    request: Annotated[LoginRequest, Body()], service: Annotated[AdminService, Depends()]
) -> LoginUserResponse:
    return await service.login(**request.dict())


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
    response_description="",
    name="get self",
    description="get self",
)
async def get_self(user: Annotated[UserModel, Depends(HasPermission(RoleType.ADMIN))]) -> UserModel:
    return user


@router.post(
    "/create_user",
    status_code=status.HTTP_200_OK,
    response_model=AdminUserResponse,
    response_description="",
    name="admin create user",
    description="create user",
)
async def create_user(
    request: Annotated[AdminCreateUserRequest, Body()],
    service: Annotated[AdminService, Depends()],
    user: Annotated[UserModel, Depends(HasPermission(RoleType.ADMIN))],
) -> AdminUserResponse:
    return await service.create_user(**request.dict())
