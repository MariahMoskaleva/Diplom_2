import pytest
import uuid
import allure

from models.responses import (
    CreateOrderSuccessResponse,
    CreateOrderErrorResponse,
    IngredientsResponse
)
from utils.validators import validate_response
from utils.orders_factory import (
    generate_order_payload,
    generate_invalid_order_payload
)


@allure.epic("Заказы")
@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа: ingredients={ingredients_mode}, auth={use_auth}")
    @pytest.mark.parametrize(
        "ingredients_mode, use_auth, expected_status, expected_model",
        [
            ("valid", True, 200, CreateOrderSuccessResponse),
            ("valid", False, 200, CreateOrderSuccessResponse),
            ("empty", True, 400, CreateOrderErrorResponse),
            ("missing", True, 400, CreateOrderErrorResponse),
            ("invalid", True, 500, None),
        ]
    )
    def test_create_order(
        self, api_client, create_user, get_ingredient_ids,
        ingredients_mode, use_auth, expected_status, expected_model
    ):
        with allure.step("Формирование заголовков авторизации"):
            headers = {}
            if use_auth:
                user = create_user
                headers["Authorization"] = user.access_token

        with allure.step(f"Формирование payload: ingredients_mode = '{ingredients_mode}'"):
            if ingredients_mode == "valid":
                payload = generate_order_payload(get_ingredient_ids[:2])
            elif ingredients_mode == "invalid":
                payload = generate_invalid_order_payload()
            elif ingredients_mode == "empty":
                payload = generate_order_payload([])
            elif ingredients_mode == "missing":
                payload = {}

        with allure.step("Отправка POST-запроса на /orders"):
            response = api_client.post("/orders", json=payload, headers=headers)

        with allure.step(f"Проверка статус-кода == {expected_status}"):
            assert response.status_code == expected_status, f"Unexpected status: {response.text}"

        if expected_model:
            with allure.step("Валидация тела ответа по Pydantic-схеме"):
                body = validate_response(response, {expected_status: expected_model})
                assert body.success is (expected_status == 200)
        else:
            with allure.step("Ошибка без валидации (ожидаемое исключение/500)"):
                allure.attach(response.text, name="RAW RESPONSE", attachment_type=allure.attachment_type.TEXT)
