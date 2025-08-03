import pytest
import allure
import requests
from endpoints.meme import MemeEndpoint
from endpoints.authorize import AuthorizeEndpoint


@pytest.mark.negative
@allure.feature("Negative Tests")
@allure.title("Авторизация с пустым телом запроса (ожидается 400)")
@allure.severity(allure.severity_level.MINOR)
def test_authorize_with_empty_body():
    endpoint = AuthorizeEndpoint()
    with allure.step("Попытка авторизации с пустым телом запроса"):
        endpoint.post_authorize(json={})
        endpoint.check_status_code(400)
        assert endpoint.last_data, "Response body is empty"
        if isinstance(endpoint.last_data, dict):
            assert "error" in endpoint.last_data or "message" in endpoint.last_data
        else:
            assert "Bad Request" in endpoint.last_data or "Invalid" in endpoint.last_data


@pytest.mark.negative
@allure.feature("Negative Tests")
@allure.title("Доступ с невалидным токеном (ожидается 401 Unauthorized)")
@allure.severity(allure.severity_level.CRITICAL)
def test_get_memes_with_invalid_token():
    endpoint = MemeEndpoint()
    endpoint.headers["Authorization"] = "Bearer INVALID"
    with allure.step("Попытка получить мемы с невалидным токеном"):
        response = requests.get(f"{endpoint.base_url}/meme", headers=endpoint.headers)
        assert response.status_code == 401


@pytest.mark.negative
@allure.feature("Negative Tests")
@allure.title("Создание мема без обязательных полей (ожидается 400)")
@allure.severity(allure.severity_level.NORMAL)
def test_create_meme_with_missing_fields(meme_endpoint):
    with allure.step("Создание мема с пустым телом запроса"):
        meme_endpoint.last_response = requests.post(
            f"{meme_endpoint.base_url}/meme", json={}, headers=meme_endpoint.headers
        )
        meme_endpoint.check_status_code(400)


@pytest.mark.negative
@allure.feature("Negative Tests")
@allure.title("Получение несуществующего мема (ожидается 404)")
@allure.severity(allure.severity_level.NORMAL)
def test_get_nonexistent_meme(meme_endpoint):
    meme_endpoint.get_one(9999999)
    meme_endpoint.check_status_code(404)


@pytest.mark.negative
@allure.feature("Negative Tests")
@allure.title("Удаление несуществующего мема (ожидается 404)")
@allure.severity(allure.severity_level.NORMAL)
def test_delete_nonexistent_meme(meme_endpoint):
    meme_endpoint.delete(9999999)
    meme_endpoint.check_status_code(404)


@pytest.mark.negative
@allure.feature("Negative Tests")
@allure.title("Создание/обновление мема с некорректными типами полей (ожидается 400)")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize(
    "payload, method, path",
    [
        (
            {
                "text": "Invalid Meme",
                "url": "http://example.com/meme.jpg",
                "tags": {"not": "an array"},
                "info": {"author": "QA"},
            },
            "POST",
            "/meme"
        ),
        (
                {
                    "text": "Invalid Meme",
                    "url": "http://example.com/meme.jpg",
                    "tags": ["tag1", "tag2"],
                    "info": ["not", "an", "object"]
                },
            "POST",
            "/meme"
        ),
        (
            lambda meme_id: {
                "id": meme_id,
                "text": "Updated Invalid Meme",
                "url": "http://example.com/updated.jpg",
                "tags": {"invalid": "json"},
                "info": {"author": "QA"}
            },
            "PUT",
            "/meme/{id}",
        ),
        (
            lambda meme_id: {
                "id": meme_id,
                "text": "Updated Invalid Meme",
                "url": "http://example.com/updated.jpg",
                "tags": ["valid", "tags"],
                "info": ["not", "an", "object"]
            },
            "PUT",
            "/meme/{id}",
        ),
    ],
)
def test_meme_payload_type_validation(meme_endpoint, payload, method, path, request):
    if callable(payload):
        meme_id = request.getfixturevalue("temp_meme")
        payload = payload(meme_id)
        url = f"{meme_endpoint.base_url}{path.format(id=meme_id)}"
    else:
        url = f"{meme_endpoint.base_url}{path}"

    meme_endpoint.last_response = requests.request(
        method, url, json=payload, headers=meme_endpoint.headers
    )
    meme_endpoint.check_status_code(400)
