import pytest
import allure
from constants import USER_NAME

@pytest.mark.positive
@allure.feature("Authorization")
@allure.title("Успешная авторизация с валидным именем пользователя")
@allure.severity(allure.severity_level.CRITICAL)
def test_authorize_success(authorize_endpoint):
    with allure.step(f"Авторизация пользователя '{USER_NAME}'"):
        authorize_endpoint.post_authorize(USER_NAME)
        authorize_endpoint.check_status_code(200)

    with allure.step("Проверка наличия токена в ответе"):
        authorize_endpoint.validate_token()

    token = authorize_endpoint.last_data['token']

    with allure.step("Проверка валидности полученного токена"):
        authorize_endpoint.check_token(token)
        authorize_endpoint.check_status_code(200)
