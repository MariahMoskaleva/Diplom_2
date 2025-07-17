import random
import string
import uuid

from faker import Faker

fake = Faker()


def generate_password(length=8):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))


def generate_user_data():
    return {
        "email": f"user_{uuid.uuid4()}@test.com",
        "password": generate_password(),
        "name": fake.first_name()
    }


def generate_invalid_user_data(missing_fields=None):
    invalid_payload = {
        "email": fake.unique.email(),
        "password": generate_password(),
        "name": fake.first_name()
    }

    if missing_fields:
        for field in missing_fields:
            invalid_payload.pop(field)

    return invalid_payload


def generate_new_user_data_for_update(actual_payload, changing_fields):
    updated_payload = actual_payload.copy()
    updated_payload.update(changing_fields)
    return updated_payload

