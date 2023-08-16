import secrets
from datetime import datetime
from typing import Annotated

from fastapi import Depends
from pydantic import EmailStr

from app.app.errors.errors import DuplicateEmailException, UserNotFoundException, InvalidCredentialsException
from app.app.models.user import UserModel
from app.app.repositories.repository import Repository
from app.app.schemas.response import LoginUserResponse, AdminUserResponse
from app.app.types import Gender
from config import settings
from core.auth import access, refresh
from core.types import RoleType
from core.utils.hashing import Hash
from core.utils.referral_code import invite_code


class AdminService:
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

    async def login(self, email: str, password: str) -> LoginUserResponse:
        user = await self.user_repo.get(model=UserModel, with_field=UserModel.email, with_field_value=email)
        if not user:
            raise UserNotFoundException
        if user.role != RoleType.ADMIN:
            raise InvalidCredentialsException

        if not Hash.verify(hashed=user.password, raw=password):
            raise InvalidCredentialsException

        access_token = access.encode(payload={"id": str(user.id)}, expire_period=settings.ACCESS_TOKEN_EXP)
        refresh_token = refresh.encode(payload={"id": str(user.id)}, expire_period=settings.REFRESH_TOKEN_EXP)

        return LoginUserResponse(access_token=access_token, refresh_token=refresh_token)

    async def create_user(
        self,
        email: EmailStr,
        first_name: str | None = None,
        last_name: str | None = None,
        phone: str | None = None,
        gender: Gender | None = None,
        date_of_birth: datetime | None = None,
        country: str | None = None,
        company: str | None = None,
    ) -> AdminUserResponse:
        if email and await self.user_repo.get(model=UserModel, with_field=UserModel.email, with_field_value=email):
            raise DuplicateEmailException
        password = secrets.token_urlsafe(15)

        # Todo:
        # will send the password on user's mail

        user = UserModel.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            gender=gender,
            date_of_birth=date_of_birth,
            password=password,
            country=country,
            company=company,
            referral_code=await invite_code(),
            admin_created=True,
            system_password=True,
            is_active=True,
        )
        user = self.user_repo.save(user)

        # it's temporary response for password only

        return AdminUserResponse(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            phone=user.phone,
            gender=user.gender,
            date_of_birth=user.date_of_birth,
            country=user.country,
            company=user.company,
            is_email_verified=user.is_email_verified,
            is_active=user.is_active,
            password=password,
            admin_created=user.admin_created,
            system_password=user.system_password,
        )
