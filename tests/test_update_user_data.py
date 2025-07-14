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

    @allure.title("Успешное обновление данных пользователя: {changing_fields}")
    @pytest.mark.parametrize(
        "changing_fields",
        [
            {"name": fake.first_name()},
            {"email": fake.unique.email()},
            {"password": generate_password()},
        ]
    )
    def test_update_user_fields_success(self, api_client, create_user, changing_fields):
        user = create_user

        old_credentials = {
            "email": user.user_data["email"],
            "password": user.user_data["password"]
        }

        with allure.step("Отправка PATCH запроса на /auth/user с обновлением данных"):
            response = api_client.patch(
                path="/auth/user",
                json=changing_fields,
                headers={"Authorization": user.access_token}
            )

        with allure.step("Валидация успешного ответа 200 и структуры"):
            body = validate_response(response, {200: UpdateUserSuccessResponse})

            for key, value in changing_fields.items():
                if key != "password":
                    assert getattr(body.user, key) == value

        if "password" in changing_fields:
            new_credentials = {
                "email": old_credentials["email"],
                "password": changing_fields["password"]
            }

            with allure.step("Авторизация с новым паролем — должна пройти"):
                login_response = api_client.post("/auth/login", json=new_credentials)
                login_body = validate_response(login_response, {200: LoginSuccessResponse})
                assert login_body.accessToken.startswith("Bearer ")

            with allure.step("Авторизация со старым паролем — должна завершиться ошибкой"):
                old_login_response = api_client.post("/auth/login", json=old_credentials)
                error_body = validate_response(old_login_response, {401: LoginNotSuccessResponse})
                assert error_body.message == "email or password are incorrect"

    @allure.title("Ошибка обновления без авторизации")
    def test_update_user_without_auth_should_fail(self, api_client):
        payload = {"name": fake.first_name()}

        with allure.step("Попытка обновления без передачи токена"):
            response = api_client.patch(
                path="/auth/user",
                json=payload,
                headers={}
            )

        with allure.step("Ожидаем 401 Unauthorized"):
            body = validate_response(response, {401: UpdateUserUnauthorizedResponse})
            assert body.success is False
            assert body.message == UPDATE_USER_WITHOUT_AUTH
