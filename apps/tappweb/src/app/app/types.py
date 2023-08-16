from enum import Enum


class Gender(int, Enum):
    """
    Gender Enum class.
    """

    MALE = 0
    FEMALE = 1
    OTHER = 2
