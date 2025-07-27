import pytest
from endpoints.meme import MemeEndpoint
from utils.helpers import random_string


@pytest.fixture(scope="session")
def meme_endpoint():
    return MemeEndpoint()


@pytest.fixture
def temp_meme(meme_endpoint):
    text = f"Meme_{random_string()}"
    url = f"http://example.com/{random_string()}"
    tags = ["fun", "test"]
    info = {"author": "QA"}
    meme_endpoint.create(text, url, tags, info).check_status_code(200)
    meme_id = meme_endpoint.last_data["id"]
    yield meme_id
    meme_endpoint.delete(meme_id)
