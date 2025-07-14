import pytest
import allure

from models.responses import LoginSuccessResponse, LoginNotSuccessResponse
from utils.constants import LOGIN_USER_INCORRECT_CREDS
from utils.user_factory import generate_invalid_user_data
from utils.validators import validate_response


@allure.epic("Авторизация")
@allure.feature("Логин пользователя")
class TestLogin:

    @allure.title("Успешный вход с валидными данными")
    def test_login_user_success(self, create_user, api_client):
        user = create_user
        email = user.user_data['email']
        password = user.user_data['password']
        payload = {"email": email, "password": password}

        with allure.step("Отправка запроса на /auth/login с корректными данными"):
            response = api_client.post(path="/auth/login", json=payload)

        with allure.step("Валидация ответа"):
            body = validate_response(response, {200: LoginSuccessResponse})
            assert body.success is True
            assert body.accessToken is not None
            assert body.refreshToken is not None
            assert body.user["email"] == email
            assert body.user["name"] is not None

    @allure.title("Ошибка при входе с некорректными данными")
    def test_login_invalid_user_not_authorized(self, api_client):
        invalid_payload = generate_invalid_user_data()

        with allure.step("Попытка входа с невалидными данными"):
            response = api_client.post(path="/auth/login", json=invalid_payload)

        with allure.step("Валидация ошибки 401"):
            body = validate_response(response, {401: LoginNotSuccessResponse})
            assert body.success is False
            assert body.message == LOGIN_USER_INCORRECT_CREDS
