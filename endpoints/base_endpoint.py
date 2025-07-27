import requests
from constants import BASE_URL
from utils.token_manager import TokenManager


class BaseEndpoint:
    def __init__(self):
        self.base_url = BASE_URL
        self.headers = {"Authorization": TokenManager.get_token()}
        self.last_response = None
        self.last_data = None

    def check_status_code(self, expected_code):
        assert self.last_response.status_code == expected_code, (
            f"Expected status code {expected_code}, got {self.last_response.status_code}"
        )
