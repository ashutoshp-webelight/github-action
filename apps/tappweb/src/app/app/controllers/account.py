from typing import Annotated

from fastapi import APIRouter, Depends, Body, status

from app.app.models.user import UserModel
from app.app.schemas import UserResponse, LoginUserResponse, CreateAccountRequest
from app.app.services import UserService
from core.auth import HasPermission
from core.types import RoleType

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=LoginUserResponse,
    response_description="",
    name="create account",
    description="create account",
)
async def create_account(
    request: Annotated[CreateAccountRequest, Body()], service: Annotated[UserService, Depends()]
) -> LoginUserResponse:
    """
    \f

    Create a account endpoint.
    :param service: User Service.
    :param request: Data of the user to be created.
    :return: Data of the created user.
    """
    return await service.create_account(**request.dict())


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
    response_description="",
    name="get self",
    description="get self",
)
async def get_self(user: Annotated[UserModel, Depends(HasPermission(RoleType.USER))]) -> UserModel:
    return user
