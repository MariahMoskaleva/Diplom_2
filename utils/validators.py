from pydantic import BaseModel, ValidationError
from models.responses import CreateUserNotSuccessResponse


class ResponseValidationError(Exception):
    pass


def validate_response(response, expected_models_by_status: dict):
    status = response.status_code
    data = response.json()

    model_class = expected_models_by_status.get(status)
    if not model_class:
        raise ResponseValidationError(f"Unexpected status code {status} with body: {data}")

    try:
        return model_class.parse_obj(data)
    except ValidationError as e:
        raise ResponseValidationError(f"Schema validation failed: {e}")
