import pytest
import allure
from endpoints.authorize import AuthorizeEndpoint
from constants import USER_NAME

@pytest.mark.positive
@allure.feature("Authorization")
@allure.title("Успешная авторизация с валидным именем пользователя")
@allure.severity(allure.severity_level.CRITICAL)
def test_authorize_success():
    endpoint = AuthorizeEndpoint()
    with allure.step(f"Аторизация пользователя '{USER_NAME}'"):
        endpoint.authorize(USER_NAME)
        endpoint.check_status_code(200)

    with allure.step("Проверка наличия токена в ответе"):
        endpoint.validate_token()

    token = endpoint.last_data['token']

    with allure.step("Проверка валидности полученного токена"):
        endpoint.check_token(token)
        endpoint.check_status_code(200)
