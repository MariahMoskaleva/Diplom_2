import pytest

from utils.user_factory import generate_invalid_user_data
from utils.validators import validate_response
from utils.constants import CREATING_EXISTING_USER_MESSAGE, CREATING_USER_WITHOUT_REQUIRED_FIELDS_MESSAGE
from models.responses import CreateUserNotSuccessResponse


class TestCreateUser:
    def test_create_unique_user_success(self, create_user):
        user_info, access_token, refresh_token = create_user
        assert access_token is not None and refresh_token is not None and user_info.get(
            "email") is not None and user_info.get("name") is not None

    def test_create_existing_user_conflict(self, create_user, api_client):
        user_info, _, _ = create_user
        payload = {"email": user_info["email"],
                   "password": "password",
                   "name": user_info["name"]}
        response = api_client.post(path="/auth/register", json=payload)
        body = validate_response(response, {403: CreateUserNotSuccessResponse})
        assert body.message == CREATING_EXISTING_USER_MESSAGE

    @pytest.mark.parametrize("missing_field", [["email"], ["password"], ["name"]])
    def test_create_user_with_missing_field_failed(self, api_client, missing_field):
        invalid_payload = generate_invalid_user_data(missing_field)
        response = api_client.post(path="/auth/register", json=invalid_payload)
        body = validate_response(response,{403: CreateUserNotSuccessResponse})
        assert body.message == CREATING_USER_WITHOUT_REQUIRED_FIELDS_MESSAGE

