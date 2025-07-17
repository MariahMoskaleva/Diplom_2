import pytest
import allure

from utils.user_factory import generate_invalid_user_data
from utils.validators import validate_response
from utils.constants import (
    CREATING_EXISTING_USER_MESSAGE,
    CREATING_USER_WITHOUT_REQUIRED_FIELDS_MESSAGE
)
from models.responses import CreateUserNotSuccessResponse


@allure.epic("Пользователь")
@allure.feature("Регистрация")
class TestCreateUser:

    @allure.title("Успешное создание уникального пользователя")
    def test_create_unique_user_success(self, create_user):
        user = create_user
        user_info = user.user_info

        with allure.step("Проверка, что токены и данные пользователя присутствуют"):
            assert user.access_token is not None
            assert user.refresh_token is not None
            assert user_info.get("email") is not None
            assert user_info.get("name") is not None

    @allure.title("Создание уже существующего пользователя — ошибка 403")
    def test_create_existing_user_conflict(self, create_user, api_client):
        user = create_user
        user_info = user.user_info

        payload = {
            "email": user_info["email"],
            "password": "password",
            "name": user_info["name"]
        }

        with allure.step("Попытка регистрации с уже существующим email"):
            response = api_client.post(path="/auth/register", json=payload)

        with allure.step("Ожидаем сообщение об ошибке 403 — пользователь уже существует"):
            body = validate_response(response, {403: CreateUserNotSuccessResponse})
            assert body.success is False
            assert body.message == CREATING_EXISTING_USER_MESSAGE

    @allure.title("Ошибка регистрации — отсутствует поле: {missing_field}")
    @pytest.mark.parametrize("missing_field", [["email"], ["password"], ["name"]])
    def test_create_user_with_missing_field_failed(self, api_client, missing_field):
        with allure.step(f"Генерация payload без поля {missing_field}"):
            invalid_payload = generate_invalid_user_data(missing_field)

        with allure.step("Отправка запроса и проверка ошибки 403"):
            response = api_client.post(path="/auth/register", json=invalid_payload)
            body = validate_response(response, {403: CreateUserNotSuccessResponse})
            assert body.message == CREATING_USER_WITHOUT_REQUIRED_FIELDS_MESSAGE
