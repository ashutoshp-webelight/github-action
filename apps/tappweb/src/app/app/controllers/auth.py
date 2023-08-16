from fastapi import APIRouter, Depends, status, Body
from pydantic import EmailStr
from typing_extensions import Annotated

from app.app.models.user import UserModel
from app.app.schemas import (
    ForgetPasswordRequest,
    ChangePasswordRequest,
    LoginUserResponse,
    UserResponse,
    MagicLinkResponse,
    LoginRequest,
)
from app.app.schemas import UserCreateRequest
from app.app.services import AuthService
from core.auth import HasPermission
from core.types import RoleType
from core.utils import SuccessResponse

router = APIRouter()


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=MagicLinkResponse,
    response_description="",
    name="Register user",
    description="Register user",
)
async def create_user(
    service: Annotated[AuthService, Depends()], request: Annotated[UserCreateRequest, Body()]
) -> MagicLinkResponse:
    """
    \f

    Create a user.
    :param service: User Service.
    :param request: Data of the user to be created.
    :return: Data of the created user.
    """
    return await service.create_user(**request.dict())


@router.get(
    "/verify",
    status_code=status.HTTP_201_CREATED,
    response_model=SuccessResponse,
    response_description="",
    name="Token verify",
    description="Token verify",
)
async def verify_token(token: str, service: Annotated[AuthService, Depends()]) -> SuccessResponse:
    """
    verify email endpoint with verification link
    :param token : str
    :param service: User Service.
    """
    return await service.verify_token(token=token)


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse | LoginUserResponse | MagicLinkResponse,
    response_description="",
    name="Login Password",
    description="",
)
async def login(
    service: Annotated[AuthService, Depends()], request: Annotated[LoginRequest, Body()]
) -> UserResponse | LoginUserResponse | MagicLinkResponse:
    """
    \f
    Login endpoint.
    :param service: User Service.
    :param request: User credentials.
    :return: Access token and Refresh Token.
    """
    return await service.login(**request.dict())


@router.post(
    "/request-forget-password",
    status_code=status.HTTP_200_OK,
    response_model=MagicLinkResponse,
    response_description="",
    name="Trigger Forget Password OTP",
    description="",
)
async def request_forget_password(service: Annotated[AuthService, Depends()], email: EmailStr) -> MagicLinkResponse:
    """
    \f
    :param email: User Email.
    :param service: User Service.
    :return: Phone and Otp.
    """
    return await service.request_forget_password(email=email)


@router.post(
    "/forget-password-verify",
    status_code=status.HTTP_200_OK,
    response_model=SuccessResponse,
    response_description="",
    name="Verify Forget Password",
    description="",
)
async def forget_password_verify(
    service: Annotated[AuthService, Depends()], request: Annotated[ForgetPasswordRequest, Body()]
) -> SuccessResponse:
    """
    \f
    Send-Otp endpoint.
    :param service: User Service.
    :param request: User Email.
    :return: Phone and Otp.
    """
    return await service.forget_password_verify(**request.dict())


@router.post(
    "/change-password",
    status_code=status.HTTP_200_OK,
    response_model=SuccessResponse,
    response_description="",
    name="change password",
    description="change password",
)
async def change_password(
    request: Annotated[ChangePasswordRequest, Body()],
    service: Annotated[AuthService, Depends()],
    user: Annotated[UserModel, Depends(HasPermission(RoleType.USER))],
) -> SuccessResponse:
    return await service.user_change_password(**request.dict(), id=user.id)
