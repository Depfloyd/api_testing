import pytest
import allure
from utils.helpers import random_string

@pytest.mark.positive
@allure.feature("Meme API")
@allure.title("Создание нового мема")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_meme(meme_endpoint):
    with allure.step("Создание нового мема"):
        meme_endpoint.create("Test Meme", "http://example.com/meme.jpg", ["test"], {"author": "me"})
        meme_endpoint.check_status_code(200)
        meme_endpoint.validate_meme(text="Test Meme")

@pytest.mark.positive
@allure.feature("Meme API")
@allure.title("Получение списка всех мемов")
@allure.severity(allure.severity_level.NORMAL)
def test_get_all_memes(meme_endpoint):
    with allure.step("Получение списка всех мемов"):
        meme_endpoint.get_all()
        meme_endpoint.check_status_code(200)

@pytest.mark.positive
@allure.feature("Meme API")
@allure.title("Получение одного мема по ID")
@allure.severity(allure.severity_level.NORMAL)
def test_get_single_meme(meme_endpoint, temp_meme):
    with allure.step("Получение одного мема по ID"):
        meme_endpoint.get_one(temp_meme)
        meme_endpoint.check_status_code(200)

@pytest.mark.positive
@allure.feature("Meme API")
@allure.title("Обновление существующего мема")
@allure.severity(allure.severity_level.NORMAL)
def test_update_meme(meme_endpoint, temp_meme):
    with allure.step("Обновление существующего мема"):
        meme_endpoint.update(
            temp_meme,
            text="Updated Meme",
            url="http://example.com/updated.jpg",
            tags=["updated"],
            info={"author": "updated_author"}
        )
        meme_endpoint.check_status_code(200)
        meme_endpoint.validate_meme(text="Updated Meme")

@pytest.mark.positive
@allure.feature("Meme API")
@allure.title("Удаление существующего мема")
@allure.severity(allure.severity_level.NORMAL)
def test_delete_meme(meme_endpoint):
    with allure.step("Создание мема для последующего удаления"):
        text = random_string()
        meme_endpoint.create(text, "http://example.com/del.jpg", ["del"], {"author": "QA"})
        meme_endpoint.check_status_code(200)
        meme_id = meme_endpoint.last_data["id"]

    with allure.step("Удаление мема"):
        meme_endpoint.delete(meme_id)
        meme_endpoint.check_status_code(200)

    with allure.step("Проверка, что мем удалён"):
        meme_endpoint.get_one(meme_id)
        meme_endpoint.check_status_code(404)
