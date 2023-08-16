import base64
import hashlib
import hmac

from config import settings


class Hash:
    """
    Class for all password related operations.
    """

    secret_key = bytes(settings.JWT_SECRET_KEY, "utf-8")

    @classmethod
    def make(cls, string: str):
        """
        Method to hash the given string.

        :param string: The string to be hashed
        :return: Hashed version of the string.
        """

        hash = hmac.new(cls.secret_key, bytes(string, "utf-8"), hashlib.sha256)
        hash.hexdigest()
        hash = base64.b64encode(hash.digest()).decode("utf-8")
        return hash

    @classmethod
    def verify(cls, hashed: str, raw: str) -> bool:
        """
        Method to verify the hash of the given string.

        :param hashed: The hashed string.
        :param raw: The string to be verified.
        :return: True if hash matches the given string, False otherwise.
        """

        return cls.make(raw) == hashed
