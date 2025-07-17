import pytest
import allure
from faker import Faker

from utils.constants import UPDATE_USER_WITHOUT_AUTH
from utils.validators import validate_response
from models.responses import (
    UpdateUserSuccessResponse,
    UpdateUserUnauthorizedResponse,
    LoginSuccessResponse,
    LoginNotSuccessResponse,
)
from utils.user_factory import generate_password

fake = Faker()


@allure.epic("Профиль пользователя")
@allure.feature("Обновление данных пользователя")
class TestUpdateUserData:

    @allure.title("Обновление имени пользователя")
    def test_update_user_name(self, api_client, create_user):
        headers = {"Authorization": create_user.access_token}
        new_name = {"name": fake.first_name()}

        response = api_client.patch("/auth/user", json=new_name, headers=headers)
        body = validate_response(response, {200: UpdateUserSuccessResponse})
        assert body.user.name == new_name["name"]

    @allure.title("Обновление email пользователя")
    def test_update_user_email(self, api_client, create_user):
        headers = {"Authorization": create_user.access_token}
        new_email = {"email": fake.unique.email()}

        response = api_client.patch("/auth/user", json=new_email, headers=headers)
        body = validate_response(response, {200: UpdateUserSuccessResponse})
        assert body.user.email == new_email["email"]

    @allure.title("Обновление пароля пользователя")
    def test_update_user_password(self, api_client, create_user):
        headers = {"Authorization": create_user.access_token}
        new_password = generate_password()
        new_data = {"password": new_password}

        old_credentials = {
            "email": create_user.user_data["email"],
            "password": create_user.user_data["password"]
        }

        response = api_client.patch("/auth/user", json=new_data, headers=headers)
        validate_response(response, {200: UpdateUserSuccessResponse})

        # Успешная авторизация с новым паролем
        new_login = {"email": old_credentials["email"], "password": new_password}
        login_response = api_client.post("/auth/login", json=new_login)
        login_body = validate_response(login_response, {200: LoginSuccessResponse})
        assert login_body.accessToken.startswith("Bearer ")

        # Ошибка при авторизации со старым паролем
        old_login_response = api_client.post("/auth/login", json=old_credentials)
        error_body = validate_response(old_login_response, {401: LoginNotSuccessResponse})
        assert error_body.message == "email or password are incorrect"

    @allure.title("Попытка обновить данные без авторизации")
    def test_update_user_without_auth_should_fail(self, api_client):
        payload = {"name": fake.first_name()}
        response = api_client.patch("/auth/user", json=payload, headers={})
        body = validate_response(response, {401: UpdateUserUnauthorizedResponse})
        assert body.success is False
        assert body.message == UPDATE_USER_WITHOUT_AUTH
