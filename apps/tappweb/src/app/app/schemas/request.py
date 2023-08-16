import re
from datetime import datetime, date

from dateutil.parser import parse, ParserError
from pydantic import EmailStr, field_validator
from pydantic import model_validator

import constants
from app.app.types import Gender
from core.utils import CamelCaseModel
from core.utils.password import strong_password


class UserCreateRequest(CamelCaseModel):
    """
    Request Schema for creating users."""

    email: EmailStr
    password: str

    @field_validator("password")
    def validate_password(cls, v: str) -> str:
        """
        Validation of password for creating users."""
        if not strong_password(password=v):
            raise ValueError(constants.WEAK_PASSWORD)
        return v


class CreateAccountRequest(CamelCaseModel):
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    gender: Gender | None = None
    date_of_birth: date | None = None
    country: str | None = None
    company: str | None = None

    @field_validator("first_name", "last_name")
    def validate_first_name(cls, v: str) -> str:
        """
        Validation of first_name for creating users.
        """
        if not re.search(r"^\S+\S$", v, re.I):
            raise ValueError(constants.INVALID + f"{v.replace('_', ' ')}")
        return v

    @field_validator("date_of_birth")
    def validate_date_of_birth(cls, v: datetime) -> datetime:
        """
        Validation of date of birth for creating users.
        """
        if v:
            try:
                v = str(v)
                birthdate = parse(v).combine(parse(v).date(), parse(v).time())
                today = datetime.today()
                one_or_zero = (today.month, today.day) < (birthdate.month, birthdate.day)
                year_difference = today.year - birthdate.year
                age = year_difference - one_or_zero

                if age < constants.AGE:
                    raise ValueError(constants.USER_IS_UNDERAGE)
                return birthdate
            except ParserError:
                raise ValueError(constants.INVALID_DATE_OF_BIRTH)


class LoginRequest(CamelCaseModel):
    """
    Request Schema for User login.
    """

    email: EmailStr
    password: str


class ForgetPasswordRequest(CamelCaseModel):
    """
    Request Schema for User Phone
    """

    token: str
    new_password: str
    confirm_password: str

    @field_validator("new_password")
    def validate_password(cls, v: str) -> str:
        """
        Validation of password for creating users.
        """
        if not strong_password(password=v):
            raise ValueError(constants.WEAK_PASSWORD)
        return v

    @model_validator(mode="after")
    def check_passwords_match(self):
        if self.new_password != self.confirm_password:
            raise ValueError(constants.PASSWORD_NOT_SAME)
        return self


class AdminCreateUserRequest(CamelCaseModel):
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    gender: Gender | None = None
    date_of_birth: date | None = None
    country: str | None = None
    company: str | None = None

    @field_validator("first_name", "last_name")
    def validate_first_name(cls, v: str) -> str:
        """
        Validation of first_name for creating users.
        """
        if not re.search(r"{}".format(constants.FIRST_NAME_REGEX), v, re.I):
            raise ValueError(constants.INVALID + f"{v.replace('_', ' ')}")
        return v

    @field_validator("date_of_birth")
    def validate_date_of_birth(cls, v: date) -> datetime:
        """
        Validation of date of birth for creating users.
        """
        if v:
            try:
                v = str(v)
                birthdate = parse(v).combine(parse(v).date(), parse(v).time())
                today = datetime.today()
                one_or_zero = (today.month, today.day) < (birthdate.month, birthdate.day)
                year_difference = today.year - birthdate.year
                age = year_difference - one_or_zero

                if age < constants.AGE:
                    raise ValueError(constants.USER_IS_UNDERAGE)
                return birthdate
            except ParserError:
                raise ValueError(constants.INVALID_DATE_OF_BIRTH)


class ChangePasswordRequest(CamelCaseModel):
    old_password: str
    new_password: str
    confirm_password: str

    @field_validator("new_password")
    def validate_password(cls, v: str) -> str:
        """
        Validation of password for creating users.
        """
        if not strong_password(password=v):
            raise ValueError(constants.WEAK_PASSWORD)
        return v

    @model_validator(mode="after")
    def check_passwords_match(self):
        if self.new_password != self.confirm_password:
            raise ValueError(constants.PASSWORD_NOT_SAME)

        return self
