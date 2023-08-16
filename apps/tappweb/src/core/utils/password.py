import re
from typing import Match


def strong_password(password) -> Match[str]:
    """
    Password checker.
    """

    return re.search("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$", password, re.I)
