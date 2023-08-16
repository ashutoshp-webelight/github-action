from datetime import date
from typing import Optional
from uuid import UUID

from core.utils import CamelCaseModel


class UserResponse(CamelCaseModel):
    id: UUID
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    gender: Optional[int]
    date_of_birth: Optional[date]
    country: Optional[str]
    company: Optional[str]
    is_email_verified: Optional[bool]
    is_active: Optional[bool]
    admin_created: Optional[bool]
    system_password: Optional[bool]


class LoginUserResponse(CamelCaseModel):
    """
    Response Schema for User login.
    """

    access_token: str
    refresh_token: str


class MagicLinkResponse(CamelCaseModel):
    link: str
    message: str


class AdminUserResponse(UserResponse):
    """
    # Note : It's temporary once email services will integrate it will be removed system_password
    """

    password: str
