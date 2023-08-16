import constants
from core.exceptions import (
    AlreadyExistsError,
    BadRequestError,
    UnauthorizedError,
    ForbiddenError,
    UnprocessableEntityError,
)


class DuplicateEmailException(AlreadyExistsError):
    """
    Custom exception for email duplication.
    """

    message = constants.DUPLICATE_EMAIL


class DuplicatePhoneException(AlreadyExistsError):
    """
    Custom exception for phone number duplication.
    """

    message = constants.DUPLICATE_PHONE


class UserNotFoundException(BadRequestError):
    """
    Custom exception for user not found error.
    """

    message = constants.USER_NOT_FOUND


class AccountAlreadyCreated(BadRequestError):
    message = constants.ACCOUNT_ALREADY_CREATED


class TooManyInvalidAuthenticationException(BadRequestError):
    """
    Custom exception for attempt Invalid credentials for user authentication.
    """

    message = constants.TOO_MANY_WRONG_ATTEMPTS


class InvalidCredentialsException(UnauthorizedError):
    """
    Custom exception to show a generic error message.
    """

    message = constants.INVALID_CREDS


class UnVerifiedException(ForbiddenError):
    """
    Custom exception to show a generic error message.
    """

    message = constants.USER_UNVERIFIED


class OTPExpireException(UnauthorizedError):
    """
    Custom exception for otp expire.
    """

    message = constants.OTP_EXPIRED


class InvalidOTPException(UnauthorizedError):
    """
    Custom exception for otp Invalid.
    """

    message = constants.INVALID_OTP


class InvalidTokenException(UnprocessableEntityError):
    """
    Returns :class:`JSONResponse` with desired status code.
    """

    message = constants.INVALID_TOKEN


class LinkExpiredException(BadRequestError):
    message = constants.LINK_EXPIRED
