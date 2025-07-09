import pytest
import requests

from api_client.api_wrapper import ApiClient
from utils.user_factory import generate_user_data


@pytest.fixture
def api_client():
    api_client = ApiClient()
    return api_client


@pytest.fixture()
def create_user(api_client):
    user_data = generate_user_data()
    response = api_client.post(path="/auth/register", json=user_data)
    if response.status_code == 200:
        user_info = response.json().get("user")
        access_token = response.json().get("accessToken")
        refresh_token = response.json().get("refreshToken")
    yield user_info, access_token, refresh_token
    if access_token:
        api_client.delete(path="/auth/user", headers={'Authorization': access_token})