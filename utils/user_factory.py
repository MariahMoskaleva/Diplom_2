import random
import string

from faker import Faker

fake = Faker()


def generate_password(length=8):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))


def generate_user_data():
    return {
        "email": fake.email(),
        "password": generate_password(),
        "name": fake.first_name()
    }


def generate_invalid_user_data(missing_fields: list):
    invalid_payload = {
        "email": fake.email(),
        "password": generate_password(),
        "name": fake.first_name()
    }

    for field in missing_fields:
        invalid_payload.pop(field)

    return invalid_payload
