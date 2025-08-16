import pytest
import allure


@pytest.mark.negative
@allure.feature("Negative Tests")
@allure.title("Авторизация с пустым телом запроса (ожидается 400)")
@allure.severity(allure.severity_level.MINOR)
def test_authorize_with_empty_body(authorize_endpoint):
    with allure.step("Попытка авторизации с пустым телом запроса"):
        authorize_endpoint.post_authorize({})
        authorize_endpoint.check_status_code(400)
        authorize_endpoint.validate_empty_body_error()


@pytest.mark.negative
@allure.feature("Negative Tests")
@allure.title("Доступ с невалидным токеном (ожидается 401 Unauthorized)")
@allure.severity(allure.severity_level.CRITICAL)
def test_get_memes_with_invalid_token(meme_endpoint):
    with allure.step("Попытка получить мемы с невалидным токеном"):
        meme_endpoint.get_with_invalid_token("INVALID")
        meme_endpoint.check_status_code(401)
        meme_endpoint.validate_unauthorized_error()


@pytest.mark.negative
@allure.feature("Negative Tests")
@allure.title("Создание мема без обязательных полей (ожидается 400)")
@allure.severity(allure.severity_level.NORMAL)
def test_create_meme_with_missing_fields(meme_endpoint):
    with allure.step("Создание мема с пустым телом запроса"):
        meme_endpoint.create_with_custom_payload({})
        meme_endpoint.check_status_code(400)


@pytest.mark.negative
@allure.feature("Negative Tests")
@allure.title("Получение несуществующего мема (ожидается 404)")
@allure.severity(allure.severity_level.NORMAL)
def test_get_nonexistent_meme(meme_endpoint):
    with allure.step("Попытка получить несуществующий мем по ID 9999999"):
        meme_endpoint.get_one(9999999)
        meme_endpoint.check_status_code(404)


@pytest.mark.negative
@allure.feature("Negative Tests")
@allure.title("Удаление несуществующего мема (ожидается 404)")
@allure.severity(allure.severity_level.NORMAL)
def test_delete_nonexistent_meme(meme_endpoint):
    with allure.step("Попытка удалить несуществующий мем по ID 9999999"):
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
    with allure.step(f"Отправка {method} запроса с некорректными типами полей"):
        url, final_payload = meme_endpoint.prepare_payload_url(payload, path, request)
        
        # Извлекаем только путь из URL для метода make_request
        endpoint = url.replace(meme_endpoint.base_url, "")
        meme_endpoint.make_request(method, endpoint, final_payload)
        meme_endpoint.check_status_code(400)


@pytest.mark.unauthorized
@allure.feature("Unauthorized Access")
@allure.title("Получение списка мемов без токена авторизации")
@allure.severity(allure.severity_level.CRITICAL)
def test_get_all_memes_without_token(unauthorized_endpoint):
    with allure.step("Попытка получить список мемов без токена авторизации"):
        unauthorized_endpoint.get_all()
        unauthorized_endpoint.check_status_code(401)


@pytest.mark.unauthorized
@allure.feature("Unauthorized Access")
@allure.title("Получение мема по ID без токена авторизации")
@allure.severity(allure.severity_level.CRITICAL)
def test_get_meme_by_id_without_token(unauthorized_endpoint):
    with allure.step("Попытка получить мем по ID без токена авторизации"):
        unauthorized_endpoint.get_one(1)
        unauthorized_endpoint.check_status_code(401)


@pytest.mark.unauthorized
@allure.feature("Unauthorized Access")
@allure.title("Создание мема без токена авторизации")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_meme_without_token(unauthorized_endpoint):
    with allure.step("Попытка создать мем без токена авторизации"):
        unauthorized_endpoint.create(
            "Test Meme", 
            "http://example.com/meme.jpg", 
            ["test"], 
            {"author": "me"}
        )
        unauthorized_endpoint.check_status_code(401)


@pytest.mark.unauthorized
@allure.feature("Unauthorized Access")
@allure.title("Обновление мема без токена авторизации")
@allure.severity(allure.severity_level.CRITICAL)
def test_update_meme_without_token(unauthorized_endpoint):
    with allure.step("Попытка обновить мем без токена авторизации"):
        unauthorized_endpoint.update(
            1,
            "Updated Meme", 
            "http://example.com/updated.jpg", 
            ["updated"], 
            {"author": "updated_author"}
        )
        unauthorized_endpoint.check_status_code(401)


@pytest.mark.unauthorized
@allure.feature("Unauthorized Access")
@allure.title("Удаление мема без токена авторизации")
@allure.severity(allure.severity_level.CRITICAL)
def test_delete_meme_without_token(unauthorized_endpoint):
    with allure.step("Попытка удалить мем без токена авторизации"):
        unauthorized_endpoint.delete(1)
        unauthorized_endpoint.check_status_code(401)


@pytest.mark.unauthorized
@allure.feature("Unauthorized Access")
@allure.title("Получение списка мемов с невалидным токеном")
@allure.severity(allure.severity_level.CRITICAL)
def test_get_all_memes_with_invalid_token(unauthorized_endpoint):
    with allure.step("Попытка получить список мемов с невалидным токеном"):
        headers = {"Authorization": "Bearer INVALID_TOKEN_12345"}
        unauthorized_endpoint.get_all(headers=headers)
        unauthorized_endpoint.check_status_code(401)


@pytest.mark.unauthorized
@allure.feature("Unauthorized Access")
@allure.title("Получение мема по ID с невалидным токеном")
@allure.severity(allure.severity_level.CRITICAL)
def test_get_meme_by_id_with_invalid_token(unauthorized_endpoint):
    with allure.step("Попытка получить мем по ID с невалидным токеном"):
        headers = {"Authorization": "Bearer INVALID_TOKEN_12345"}
        unauthorized_endpoint.get_one(1, headers=headers)
        unauthorized_endpoint.check_status_code(401)


@pytest.mark.unauthorized
@allure.feature("Unauthorized Access")
@allure.title("Создание мема с невалидным токеном")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_meme_with_invalid_token(unauthorized_endpoint):
    with allure.step("Попытка создать мем с невалидным токеном"):
        headers = {"Authorization": "Bearer INVALID_TOKEN_12345"}
        unauthorized_endpoint.create(
            "Test Meme", 
            "http://example.com/meme.jpg", 
            ["test"], 
            {"author": "me"},
            headers=headers
        )
        unauthorized_endpoint.check_status_code(401)


@pytest.mark.unauthorized
@allure.feature("Unauthorized Access")
@allure.title("Обновление мема с невалидным токеном")
@allure.severity(allure.severity_level.CRITICAL)
def test_update_meme_with_invalid_token(unauthorized_endpoint):
    with allure.step("Попытка обновить мем с невалидным токеном"):
        headers = {"Authorization": "Bearer INVALID_TOKEN_12345"}
        unauthorized_endpoint.update(
            1,
            "Updated Meme", 
            "http://example.com/updated.jpg", 
            ["updated"], 
            {"author": "updated_author"},
            headers=headers
        )
        unauthorized_endpoint.check_status_code(401)


@pytest.mark.unauthorized
@allure.feature("Unauthorized Access")
@allure.title("Удаление мема с невалидным токеном")
@allure.severity(allure.severity_level.CRITICAL)
def test_delete_meme_with_invalid_token(unauthorized_endpoint):
    with allure.step("Попытка удалить мем с невалидным токеном"):
        headers = {"Authorization": "Bearer INVALID_TOKEN_12345"}
        unauthorized_endpoint.delete(1, headers=headers)
        unauthorized_endpoint.check_status_code(401)


@pytest.mark.unauthorized
@allure.feature("Unauthorized Access")
@allure.title("Получение списка мемов с пустым токеном")
@allure.severity(allure.severity_level.CRITICAL)
def test_get_all_memes_with_empty_token(unauthorized_endpoint):
    with allure.step("Попытка получить список мемов с пустым токеном"):
        headers = {"Authorization": ""}
        unauthorized_endpoint.get_all(headers=headers)
        unauthorized_endpoint.check_status_code_in_range([401, 500])


@pytest.mark.unauthorized
@allure.feature("Unauthorized Access")
@allure.title("Получение мема по ID с пустым токеном")
@allure.severity(allure.severity_level.CRITICAL)
def test_get_meme_by_id_with_empty_token(unauthorized_endpoint):
    with allure.step("Попытка получить мем по ID с пустым токеном"):
        headers = {"Authorization": ""}
        unauthorized_endpoint.get_one(1, headers=headers)
        unauthorized_endpoint.check_status_code_in_range([401, 500])


@pytest.mark.unauthorized
@allure.feature("Unauthorized Access")
@allure.title("Создание мема с пустым токеном")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_meme_with_empty_token(unauthorized_endpoint):
    with allure.step("Попытка создать мем с пустым токеном"):
        headers = {"Authorization": ""}
        unauthorized_endpoint.create(
            "Test Meme", 
            "http://example.com/meme.jpg", 
            ["test"], 
            {"author": "me"},
            headers=headers
        )
        unauthorized_endpoint.check_status_code_in_range([401, 500])


@pytest.mark.unauthorized
@allure.feature("Unauthorized Access")
@allure.title("Обновление мема с пустым токеном")
@allure.severity(allure.severity_level.CRITICAL)
def test_update_meme_with_empty_token(unauthorized_endpoint):
    with allure.step("Попытка обновить мем с пустым токеном"):
        headers = {"Authorization": ""}
        unauthorized_endpoint.update(
            1,
            "Updated Meme", 
            "http://example.com/updated.jpg", 
            ["updated"], 
            {"author": "updated_author"},
            headers=headers
        )
        unauthorized_endpoint.check_status_code_in_range([401, 500])


@pytest.mark.unauthorized
@allure.feature("Unauthorized Access")
@allure.title("Удаление мема с пустым токеном")
@allure.severity(allure.severity_level.CRITICAL)
def test_delete_meme_with_empty_token(unauthorized_endpoint):
    with allure.step("Попытка удалить мем с пустым токеном"):
        headers = {"Authorization": ""}
        unauthorized_endpoint.delete(1, headers=headers)
        unauthorized_endpoint.check_status_code_in_range([401, 500])
