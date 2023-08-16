import secrets
from datetime import datetime
from typing import Optional, Annotated
from uuid import UUID

from fastapi import Depends, status
from pydantic import EmailStr

import constants
from app.app.errors.errors import (
    UserNotFoundException,
    InvalidCredentialsException,
    LinkExpiredException,
    DuplicateEmailException,
)
from app.app.models.user import UserModel
from app.app.repositories.repository import Repository
from app.app.schemas.response import LoginUserResponse, MagicLinkResponse, UserResponse
from app.app.types import Gender
from config import settings
from core.auth import access, refresh
from core.utils import SuccessResponse, logger
from core.utils.hashing import Hash
from core.utils.redis import redis
from core.utils.referral_code import invite_code


class AuthService:
    """
    Service with methods to set and get values.
    """

    def __init__(self, repo: Annotated[Repository, Depends()]) -> None:
        """
        Call method to inject Service as a dependency.
        This method also calls a Repo instance which is injected here.

        :param repo: Repository instance.
        :return: Service Generator.
        """
        self.user_repo = repo

    async def create_user(
        self,
        email: EmailStr,
        password: str,
        first_name: str | None = None,
        last_name: str | None = None,
        phone: str | None = None,
        gender: Gender | None = None,
        date_of_birth: datetime | None = None,
        country: str | None = None,
        company: str | None = None,
    ) -> MagicLinkResponse:
        """
        Create a user.

        :param first_name: First Name
        :param last_name: Last Name
        :param email: Email Address
        :param gender: Gender
        :param country: Country Code
        :param date_of_birth: Date of Birth
        :param phone: Phone Number
        :param password: Password
        :param company: Company name
        :param role: User role
        :return: Created user model instance.
        """
        if email and await self.user_repo.get(model=UserModel, with_field=UserModel.email, with_field_value=email):
            raise DuplicateEmailException

        user = UserModel.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            password=password,
            gender=gender,
            date_of_birth=date_of_birth,
            country=country,
            company=company,
            referral_code=await invite_code(),
        )
        user = self.user_repo.save(user)
        verification_token = secrets.token_urlsafe(32)
        verification_link = f"{settings.VARIFICATION_LINK_URL}?token={verification_token}"
        await redis.set(name=verification_token, value=user.email, ex=constants.MAGIC_LINK_EXPIRED)

        # Todo will share the verification link in user's email
        return MagicLinkResponse(link=verification_link, message=constants.MAGIC_LINK_SEND_ON_EMAIL)

    async def verify_token(self, token: str) -> SuccessResponse:
        email = await redis.get(token)
        if email:
            email = email.decode("utf-8")
            response = await self.user_repo.get(UserModel, with_field=UserModel.email, with_field_value=email)
            if response:
                response.is_email_verified = True
                await redis.delete(token)
                return SuccessResponse(status=status.HTTP_200_OK, message="Email verified successfully")
        else:
            raise LinkExpiredException

    async def login(
        self, email: str, password: Optional[str] = None
    ) -> UserResponse | LoginUserResponse | MagicLinkResponse:
        """
        Login function for admin. OTP triggering for simple users and OTP verification.

        :param email: User email id
        :param password: Password
        :param otp: Otp
        :return: Token or otp based on the logging in user
        """
        user = await self.user_repo.get(model=UserModel, with_field=UserModel.email, with_field_value=email)
        if not user:
            raise UserNotFoundException

        if password:
            if not Hash.verify(hashed=user.password, raw=password):
                raise InvalidCredentialsException

        # it's for only which user which is created_by_admin
        if user.admin_created and user.system_password:
            user.is_email_verified = True

        if not user.is_email_verified:
            verification_token = secrets.token_urlsafe(32)
            verification_link = f"{settings.VARIFICATION_LINK_URL}?token={verification_token}"
            await redis.set(name=verification_token, value=user.email, ex=constants.MAGIC_LINK_EXPIRED)

            # Todo will share the verification link in user's email
            return MagicLinkResponse(link=verification_link, message=constants.MAGIC_LINK_SEND_ON_EMAIL)

        if not user.is_active:
            return user

        access_token = access.encode(payload={"id": str(user.id)}, expire_period=settings.ACCESS_TOKEN_EXP)
        refresh_token = refresh.encode(payload={"id": str(user.id)}, expire_period=settings.REFRESH_TOKEN_EXP)
        return LoginUserResponse(access_token=access_token, refresh_token=refresh_token)

    async def request_forget_password(self, email: EmailStr) -> MagicLinkResponse:
        """
        Create or update otp in Redis Db.

        :param email: email of the user
        :param otp: Otp
        :param is_verify: boolean value
        :return: (otp and email) or JSONResponse.
        """
        user = await self.user_repo.get(model=UserModel, with_field=UserModel.email, with_field_value=email)
        if not user:
            raise UserNotFoundException
        verification_token = secrets.token_urlsafe(32)
        verification_link = f"{settings.VARIFICATION_LINK_URL}?token={verification_token}"

        await redis.set(name=verification_token, value=user.email, ex=constants.MAGIC_LINK_EXPIRED)

        # Todo will share the link in user's email
        return MagicLinkResponse(link=verification_link, message=constants.MAGIC_LINK_SEND_ON_EMAIL)

    async def forget_password_verify(self, token: str, new_password: str, confirm_password: str) -> SuccessResponse:
        """
        :param email: email of the user
        :param otp: Otp
        :param new_password: New password for user
        :return: JSONResponse
        """
        email = await redis.get(token)
        if not email:
            raise LinkExpiredException
        email = email.decode("utf-8")

        user = await self.user_repo.get(model=UserModel, with_field=UserModel.email, with_field_value=email)
        if not user:
            raise UserNotFoundException

        user.password = Hash.make(string=new_password)
        await redis.delete(token)
        logger.name = f"User: '{user}' password changed."

        return SuccessResponse(message=constants.PASSWORD_RESET_SUCCESSFULLY)

    async def user_change_password(
        self, old_password: str, new_password: str, confirm_password: str, id: UUID
    ) -> SuccessResponse:
        user = await self.user_repo.get(model=UserModel, with_field=UserModel.id, with_field_value=id)
        if not user:
            raise UserNotFoundException
        if not Hash.verify(hashed=user.password, raw=old_password):
            raise InvalidCredentialsException(message=constants.OLD_PASSWORD_NOT_MATCH)
        user.password = Hash.make(string=new_password)

        # specific for system generated password user
        if user.admin_created and user.system_password:
            user.system_password = False
        return SuccessResponse(message=constants.PASSWORD_CHANGE_SUCCESSFULLY)
