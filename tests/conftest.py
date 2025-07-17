import pytest
import requests

from api_client.api_wrapper import ApiClient
from models.responses import IngredientsResponse
from utils.orders_factory import generate_order_payload
from utils.user_factory import generate_user_data

from models.user import User
from utils.validators import validate_response


@pytest.fixture
def api_client():
    return ApiClient()


@pytest.fixture()
def create_user(api_client):
    def _create_user():
        user_data = generate_user_data()
        response = api_client.post("/auth/register", json=user_data)
        data = response.json()

        if response.status_code != 200 or "user" not in data:
            return None

        return User(
            user_info=data["user"],
            access_token=data["accessToken"],
            refresh_token=data["refreshToken"],
            user_data=user_data
        )

    user = _create_user()

    yield user

    if user:
        api_client.delete("/auth/user", headers={"Authorization": f"Bearer {user.access_token}"})


@pytest.fixture
def create_order(api_client, get_ingredient_ids):
    created_order_numbers = []

    def _create_order(auth_token=None):
        headers = {}
        if auth_token:
            headers["Authorization"] = auth_token

        ingredients = get_ingredient_ids[:2]
        payload = generate_order_payload(ingredients)

        response = api_client.post("/orders", json=payload, headers=headers)
        if response.status_code == 200:
            order_number = response.json().get("order", {}).get("number")
            if order_number:
                created_order_numbers.append(order_number)
        return response

    yield _create_order


@pytest.fixture
def get_ingredient_ids(api_client):
    response = api_client.get("/ingredients")
    body = validate_response(response, {200: IngredientsResponse})
    return [item.id for item in body.data if item.id]
