import uuid
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column
from typing_extensions import Self

from app.app.types import Gender
from core.db import Base
from core.types import RoleType
from core.utils.hashing import Hash
from core.utils.mixins import TimeStampMixin


class UserModel(Base, TimeStampMixin):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    first_name: Mapped[Optional[str]] = mapped_column(index=True)
    last_name: Mapped[Optional[str]] = mapped_column(index=True)
    email: Mapped[str] = mapped_column(index=True, unique=True)
    phone: Mapped[Optional[str]] = mapped_column(index=True, unique=True)
    password: Mapped[str] = mapped_column()
    gender: Mapped[Optional[int]] = mapped_column()
    date_of_birth: Mapped[Optional[datetime]] = mapped_column()
    country: Mapped[Optional[str]] = mapped_column()
    company: Mapped[Optional[str]] = mapped_column()
    is_email_verified: Mapped[bool] = mapped_column(default=False)
    role: Mapped[Optional[int]] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=False)
    stripe_customer_id: Mapped[Optional[str]] = mapped_column()
    referral_code: Mapped[str] = mapped_column()
    admin_created: Mapped[bool] = mapped_column(default=False, nullable=True)
    system_password: Mapped[Optional[bool]] = mapped_column(nullable=True)

    def __str__(self) -> str:
        return f"<{self.first_name} {self.last_name}>"

    @classmethod
    def create(
        cls,
        email: str,
        password: str,
        referral_code: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        phone: Optional[str] = None,
        gender: Optional[Gender] = None,
        date_of_birth: Optional[datetime] = None,
        country: Optional[str] = None,
        company: Optional[str] = None,
        is_email_verified: Optional[bool] = False,
        stripe_customer_id: Optional[str] = None,
        admin_created: Optional[bool] = None,
        system_password: Optional[bool] = None,
        is_active: Optional[bool] = False,
        role: Optional[int] = RoleType.USER,
    ) -> Self:
        return cls(
            id=uuid4(),
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            password=Hash.make(string=password),
            gender=gender,
            date_of_birth=date_of_birth,
            country=country,
            company=company,
            is_email_verified=is_email_verified,
            is_active=is_active,
            role=role,
            stripe_customer_id=stripe_customer_id,
            referral_code=referral_code,
            admin_created=admin_created,
            system_password=system_password,
        )
