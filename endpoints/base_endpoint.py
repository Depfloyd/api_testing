import requests
from constants import BASE_URL
from utils.token_manager import TokenManager
from utils.logger import setup_logger


class BaseEndpoint:
    def __init__(self):
        self.base_url = BASE_URL
        self.headers = {"Authorization": TokenManager.get_token()}
        self.last_response = None
        self.last_data = None
        self.logger = setup_logger(self.__class__.__name__)

    def check_status_code(self, expected_code):
        actual_code = self.last_response.status_code
        assert actual_code == expected_code, (
            f"Expected status code {expected_code}, got {actual_code}"
        )
        self.logger.info(f"Checked status code: {actual_code} (expected: {expected_code})")
