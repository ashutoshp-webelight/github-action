from datetime import datetime, timedelta
from typing import Any, Dict, Literal, Annotated

from fastapi import Request, Depends
from fastapi.security import HTTPBearer
from fastapi.security.utils import get_authorization_scheme_param
from jwt import DecodeError, ExpiredSignatureError, decode, encode

import constants
from app.app.errors.errors import InvalidTokenException
from app.app.models.user import UserModel
from app.app.repositories.repository import Repository
from config import settings
from core.exceptions import InvalidJWTTokenException, UnauthorizedError
from core.types import RoleType


class JWToken(HTTPBearer):
    """
    A class inheriting from :class:`HTTPBearer` to inherit the methods necessary for
    token extraction from the request.
    """

    def __init__(self, type_: Literal["access", "refresh"], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.type_ = type_

    def encode(self, payload: dict, expire_period: int = 3600) -> str:
        """
        Creates a JWT access token.

        :param payload: Claims to be included in the token.
        :param expire_period: Expiry period of the token.
        :return: JWT Token
        """
        token = encode(
            payload={**payload, "type": self.type_, "exp": datetime.utcnow() + timedelta(seconds=expire_period)},
            key=settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )
        return token

    def decode(self, _token: str) -> Dict[str, Any]:
        """
        Decode a JWT access token.

        :param _token: A JWT token.
        :return: Claims included in the token.
        """
        try:
            payload = decode(
                jwt=_token,
                key=settings.JWT_SECRET_KEY,
                algorithms=settings.JWT_ALGORITHM,
                option={"verify_signature": True, "verify_exp": True},
            )
            if payload.get("type") != self.type_:
                raise InvalidTokenException
            else:
                return payload
        except DecodeError:
            raise InvalidJWTTokenException(constants.INVALID_TOKEN)
        except ExpiredSignatureError:
            raise InvalidJWTTokenException(constants.EXPIRED_TOKEN)

    async def __call__(self, request: Request) -> Dict[str, Any]:
        """
        A magic method intercepts the request and extracts token from it.
        allowing us to access the token in the request context.

        :param request: FastAPI Request.
        :return: Claims included in the token.
        """
        authorization: str = request.headers.get("Authorization")
        scheme, credentials = get_authorization_scheme_param(authorization)
        if not (authorization and scheme and credentials):
            raise InvalidJWTTokenException(constants.UNAUTHORIZED)
        if scheme.lower() != "bearer":
            raise InvalidJWTTokenException(constants.INVALID_TOKEN)
        return self.decode(credentials)


access = JWToken(type_="access", scheme_name="JWT access token")
refresh = JWToken(type_="refresh", scheme_name="JWT refresh token")


class HasPermission:
    """
    A DependencyInjection class that checks the user type.
    """

    def __init__(self, type_: RoleType) -> None:
        """
        Initialize the object with necessary permission Enum type.

        :param type_: Type of permission to check.
        """
        self.type = type_

    async def __call__(self, user_repo: Annotated[Repository, Depends()], payload=Depends(access)) -> UserModel:
        """
        Check the user type.

        :param payload: The token payload.
        :param repo: The query object.
        :return: The user object.
        """

        user = await user_repo.get(model=UserModel, with_field=UserModel.id, with_field_value=payload.get("id"))
        if not user:
            raise InvalidTokenException
        match self.type:
            case RoleType.USER:
                if user.role == RoleType.USER:
                    return user
                raise UnauthorizedError(message=constants.UNAUTHORIZED)
            case RoleType.STAFF:
                if user.role == RoleType.STAFF:
                    return user
                raise UnauthorizedError(message=constants.UNAUTHORIZED)
            case RoleType.ADMIN:
                if user.role == RoleType.ADMIN:
                    return user
                raise UnauthorizedError(message=constants.UNAUTHORIZED)
