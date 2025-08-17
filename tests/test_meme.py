import pytest
import allure
from constants import (
    TEST_MEME_TEXT, TEST_MEME_URL, TEST_MEME_TAGS, TEST_MEME_INFO,
    UPDATED_MEME_TEXT, UPDATED_MEME_URL, UPDATED_MEME_TAGS, UPDATED_MEME_INFO
)


@pytest.mark.positive
@allure.feature("Meme API")
@allure.title("Создание нового мема")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_meme(meme_endpoint):
    with allure.step("Создание нового мема"):
        meme_endpoint.create(TEST_MEME_TEXT, TEST_MEME_URL, TEST_MEME_TAGS, TEST_MEME_INFO)
        meme_endpoint.check_status_code(200)
        meme_endpoint.validate_meme(
            text=TEST_MEME_TEXT,
            url=TEST_MEME_URL,
            tags=TEST_MEME_TAGS,
            info=TEST_MEME_INFO
        )

@pytest.mark.positive
@allure.feature("Meme API")
@allure.title("Получение списка всех мемов")
@allure.severity(allure.severity_level.NORMAL)
def test_get_all_memes(meme_endpoint):
    with allure.step("Получение списка всех мемов"):
        meme_endpoint.get_all()
        meme_endpoint.check_status_code(200)
        meme_endpoint.validate_memes_list_not_empty()

@pytest.mark.positive
@allure.feature("Meme API")
@allure.title("Получение одного мема по ID")
@allure.severity(allure.severity_level.NORMAL)
def test_get_single_meme(meme_endpoint, temp_meme):
    with allure.step("Получение одного мема по ID"):
        meme_endpoint.get_one(temp_meme)
        meme_endpoint.check_status_code(200)
        meme_endpoint.validate_meme_id(temp_meme)
        meme_endpoint.validate_meme_structure()

@pytest.mark.positive
@allure.feature("Meme API")
@allure.title("Обновление существующего мема")
@allure.severity(allure.severity_level.NORMAL)
def test_update_meme(meme_endpoint, temp_meme):
    with allure.step("Обновление существующего мема"):
        meme_endpoint.update(
            temp_meme,
            text=UPDATED_MEME_TEXT,
            url=UPDATED_MEME_URL,
            tags=UPDATED_MEME_TAGS,
            info=UPDATED_MEME_INFO
        )
        meme_endpoint.check_status_code(200)
        meme_endpoint.validate_meme(
            text=UPDATED_MEME_TEXT,
            url=UPDATED_MEME_URL,
            tags=UPDATED_MEME_TAGS,
            info=UPDATED_MEME_INFO
        )

@pytest.mark.positive
@allure.feature("Meme API")
@allure.title("Удаление существующего мема")
@allure.severity(allure.severity_level.NORMAL)
def test_delete_meme(meme_endpoint, meme_to_delete):
    meme_id = meme_to_delete

    with allure.step("Удаление мема"):
        meme_endpoint.delete(meme_id)
        meme_endpoint.check_status_code(200)

    with allure.step("Проверка, что мем удалён"):
        meme_endpoint.get_one(meme_id)
        meme_endpoint.check_status_code(404)
