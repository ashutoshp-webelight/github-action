from datetime import datetime
from typing import Annotated

from fastapi import Depends
from pydantic import EmailStr

from app.app.errors.errors import UserNotFoundException, AccountAlreadyCreated
from app.app.models.user import UserModel
from app.app.repositories.repository import Repository
from app.app.schemas.response import LoginUserResponse
from app.app.types import Gender
from config import settings
from core.auth import access, refresh


class UserService:
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

    async def create_account(
        self,
        email: EmailStr,
        first_name: str | None = None,
        last_name: str | None = None,
        phone: str | None = None,
        gender: Gender | None = None,
        date_of_birth: datetime | None = None,
        country: str | None = None,
        company: str | None = None,
    ) -> LoginUserResponse:
        user = await self.user_repo.get(model=UserModel, with_field=UserModel.email, with_field_value=email)
        if not user:
            raise UserNotFoundException

        if not user.is_active:
            user.first_name = first_name
            user.last_name = last_name
            user.phone = phone
            user.gender = gender
            user.date_of_birth = date_of_birth
            user.country = country
            user.company = company
            user.is_active = True

            access_token = access.encode(payload={"id": str(user.id)}, expire_period=settings.ACCESS_TOKEN_EXP)
            refresh_token = refresh.encode(payload={"id": str(user.id)}, expire_period=settings.REFRESH_TOKEN_EXP)
            return LoginUserResponse(access_token=access_token, refresh_token=refresh_token)
        raise AccountAlreadyCreated
