import random
import string


async def invite_code() -> str:
    length = random.randint(8, 20)

    password_chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(password_chars) for _ in range(length))
    special_char_count = sum(char in string.punctuation for char in password)
    upper_case_count = sum(char.isupper() for char in password)

    if not any((char or char.isupper()) in string.punctuation for char in password):
        return await invite_code()

    if special_char_count > 2 or upper_case_count > 2:
        return await invite_code()
    return password
