import uuid


def generate_order_payload(ingredient_ids: list[str]) -> dict:
    return {"ingredients": ingredient_ids}


def generate_invalid_order_payload() -> dict:
    return {"ingredients": [str(uuid.uuid4())]}