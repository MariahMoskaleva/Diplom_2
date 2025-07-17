import pytest
import allure

from models.responses import (
    CreateOrderSuccessResponse,
    CreateOrderErrorResponse
)
from utils.validators import validate_response
from utils.orders_factory import (
    generate_order_payload,
    generate_invalid_order_payload
)


@allure.epic("Заказы")
@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа с валидными ингредиентами и авторизацией")
    def test_create_order_with_auth_valid_ingredients(self, api_client, create_user, get_ingredient_ids):
        headers = {"Authorization": create_user.access_token}
        payload = generate_order_payload(get_ingredient_ids[:2])

        response = api_client.post("/orders", json=payload, headers=headers)
        body = validate_response(response, {200: CreateOrderSuccessResponse})
        assert body.success is True

    @allure.title("Создание заказа с валидными ингредиентами без авторизации")
    def test_create_order_without_auth_valid_ingredients(self, api_client, get_ingredient_ids):
        payload = generate_order_payload(get_ingredient_ids[:2])

        response = api_client.post("/orders", json=payload)
        body = validate_response(response, {200: CreateOrderSuccessResponse})
        assert body.success is True

    @allure.title("Создание заказа с пустым списком ингредиентов")
    def test_create_order_empty_ingredients(self, api_client, create_user):
        headers = {"Authorization": create_user.access_token}
        payload = generate_order_payload([])

        response = api_client.post("/orders", json=payload, headers=headers)
        body = validate_response(response, {400: CreateOrderErrorResponse})
        assert body.success is False

    @allure.title("Создание заказа без поля ingredients")
    def test_create_order_missing_ingredients(self, api_client, create_user):
        headers = {"Authorization": create_user.access_token}
        payload = {}

        response = api_client.post("/orders", json=payload, headers=headers)
        body = validate_response(response, {400: CreateOrderErrorResponse})
        assert body.success is False

    @allure.title("Создание заказа с невалидными ингредиентами")
    def test_create_order_invalid_ingredients(self, api_client, create_user):
        headers = {"Authorization": create_user.access_token}
        payload = generate_invalid_order_payload()

        response = api_client.post("/orders", json=payload, headers=headers)
        assert response.status_code == 500
