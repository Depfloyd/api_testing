import allure
from utils.helpers import random_string


@allure.feature("Meme API")
def test_create_meme(meme_endpoint):
    meme_endpoint.create("Test Meme", "http://example.com/meme.jpg", ["test"], {"author": "me"})
    meme_endpoint.check_status_code(200)
    meme_endpoint.validate_meme(text="Test Meme")


@allure.feature("Meme API")
def test_get_all_memes(meme_endpoint):
    meme_endpoint.get_all()
    meme_endpoint.check_status_code(200)


@allure.feature("Meme API")
def test_get_single_meme(meme_endpoint, temp_meme):
    meme_endpoint.get_one(temp_meme)
    meme_endpoint.check_status_code(200)


@allure.feature("Meme API")
def test_update_meme(meme_endpoint, temp_meme):
    meme_endpoint.update(
        temp_meme,
        text="Updated Meme",
        url="http://example.com/updated.jpg",
        tags=["updated"],
        info={"author": "updated_author"}
    )
    meme_endpoint.check_status_code(200)
    meme_endpoint.validate_meme(text="Updated Meme")


@allure.feature("Meme API")
def test_delete_meme(meme_endpoint):
    text = random_string()
    meme_endpoint.create(text, "http://example.com/del.jpg", ["del"], {"author": "QA"})
    meme_endpoint.check_status_code(200)
    meme_id = meme_endpoint.last_data["id"]
    meme_endpoint.delete(meme_id)
    meme_endpoint.check_status_code(200)
    meme_endpoint.get_one(meme_id)
    meme_endpoint.check_status_code(404)
