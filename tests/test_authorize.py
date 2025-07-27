import allure
from endpoints.authorize import AuthorizeEndpoint
from constants import USER_NAME


@allure.feature("Authorize API")
def test_authorize():
    endpoint = AuthorizeEndpoint()
    endpoint.authorize(USER_NAME)
    endpoint.check_status_code(200)
    endpoint.validate_token()
