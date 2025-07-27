import pytest
import allure
import requests
from endpoints.meme import MemeEndpoint
from endpoints.authorize import AuthorizeEndpoint


@pytest.mark.negative
@allure.feature("Negative Tests")
@allure.title("Авторизация с пустым именем (ожидается user = '')")
@allure.severity(allure.severity_level.MINOR)
def test_authorize_with_empty_name():
    endpoint = AuthorizeEndpoint()
    with allure.step("Авторизация с пустым именем"):
        endpoint.authorize("")
        endpoint.check_status_code(200)
        assert endpoint.last_data["user"] == "", "Expected user to be empty string"


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
@allure.title("Создание мема: поле tags не является массивом (ожидается 400)")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_meme_with_json_instead_of_array(meme_endpoint):
    payload = {
        "text": "Invalid Meme",
        "url": "http://example.com/meme.jpg",
        "tags": {"not": "an array"},
        "info": {"author": "QA"}
    }
    meme_endpoint.last_response = requests.post(
        f"{meme_endpoint.base_url}/meme", json=payload, headers=meme_endpoint.headers
    )
    meme_endpoint.check_status_code(400)


@pytest.mark.negative
@allure.feature("Negative Tests")
@allure.title("Создание мема: поле info передано как массив (ожидается 400)")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_meme_with_json_instead_of_object(meme_endpoint):
    payload = {
        "text": "Invalid Meme",
        "url": "http://example.com/meme.jpg",
        "tags": ["tag1", "tag2"],
        "info": ["not", "an", "object"]
    }
    meme_endpoint.last_response = requests.post(
        f"{meme_endpoint.base_url}/meme", json=payload, headers=meme_endpoint.headers
    )
    meme_endpoint.check_status_code(400)


@pytest.mark.negative
@allure.feature("Negative Tests")
@allure.title("Обновление мема: поле tags не массив (ожидается 400)")
@allure.severity(allure.severity_level.CRITICAL)
def test_update_meme_with_json_instead_of_array(meme_endpoint, temp_meme):
    payload = {
        "id": temp_meme,
        "text": "Updated Invalid Meme",
        "url": "http://example.com/updated.jpg",
        "tags": {"invalid": "json"},
        "info": {"author": "QA"}
    }
    meme_endpoint.last_response = requests.put(
        f"{meme_endpoint.base_url}/meme/{temp_meme}",
        json=payload, headers=meme_endpoint.headers
    )
    meme_endpoint.check_status_code(400)


@pytest.mark.negative
@allure.feature("Negative Tests")
@allure.title("Обновление мема: поле info передано как массив (ожидается 400)")
@allure.severity(allure.severity_level.CRITICAL)
def test_update_meme_with_array_instead_of_object(meme_endpoint, temp_meme):
    payload = {
        "id": temp_meme,
        "text": "Updated Invalid Meme",
        "url": "http://example.com/updated.jpg",
        "tags": ["valid", "tags"],
        "info": ["not", "an", "object"]
    }
    meme_endpoint.last_response = requests.put(
        f"{meme_endpoint.base_url}/meme/{temp_meme}",
        json=payload, headers=meme_endpoint.headers
    )
    meme_endpoint.check_status_code(400)
