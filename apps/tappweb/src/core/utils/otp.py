from random import randint


def otp() -> int:
    """
    Generate a random 4 digit otp

    :return: otp
    """
    random = randint(1111, 9999)
    return random
