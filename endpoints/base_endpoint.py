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

    def check_status_code_in_range(self, expected_codes):
        """Проверяет, что статус код находится в списке ожидаемых кодов"""
        actual_code = self.last_response.status_code
        assert actual_code in expected_codes, (
            f"Expected status code in {expected_codes}, got {actual_code}"
        )
        self.logger.info(f"Checked status code: {actual_code} (expected one of: {expected_codes})")

    def validate_error_response(self, expected_error_types=None):
        """Проверяет, что в ответе есть сообщение об ошибке"""
        assert self.last_data, "Response body is empty"
        
        if isinstance(self.last_data, dict):
            # Проверяем наличие полей ошибки в JSON ответе
            error_fields = expected_error_types or ["error", "message"]
            has_error_field = any(field in self.last_data for field in error_fields)
            assert has_error_field, f"Expected one of {error_fields} in response, got: {self.last_data}"
        else:
            # Проверяем текст ответа на наличие ключевых слов ошибки
            error_keywords = expected_error_types or ["Bad Request", "Invalid", "Unauthorized", "401"]
            has_error_keyword = any(keyword in str(self.last_data) for keyword in error_keywords)
            assert has_error_keyword, f"Expected one of {error_keywords} in response, got: {self.last_data}"
        
        self.logger.info(f"Validated error response: {self.last_data}")

    def validate_unauthorized_response(self):
        """Специальный метод для проверки ответов с ошибкой авторизации"""
        self.validate_error_response(["Unauthorized", "401", "error", "message"])

    def validate_unauthorized_error(self):
        """Проверяет, что в ответе есть сообщение об ошибке авторизации"""
        try:
            error_data = self.last_response.json()
            assert "error" in error_data or "message" in error_data
        except:
            # Если ответ не JSON, проверяем текст
            assert "Unauthorized" in self.last_response.text or "401" in self.last_response.text

    def prepare_payload_url(self, payload, path, request=None):
        """Подготавливает URL и payload для запросов с параметризацией"""
        if callable(payload):
            meme_id = request.getfixturevalue("temp_meme")
            payload = payload(meme_id)
            url = f"{self.base_url}{path.format(id=meme_id)}"
        else:
            url = f"{self.base_url}{path}"
        
        return url, payload
    
    def make_request(self, method, endpoint, payload=None, headers=None):
        """Универсальный метод для выполнения HTTP запросов"""
        url = f"{self.base_url}{endpoint}"
        request_headers = headers or self.headers
        
        self.logger.info(f"Выполнение {method} запроса к {url}")
        
        if method.upper() == "GET":
            self.last_response = requests.get(url, headers=request_headers)
        elif method.upper() == "POST":
            self.last_response = requests.post(url, json=payload, headers=request_headers)
        elif method.upper() == "PUT":
            self.last_response = requests.put(url, json=payload, headers=request_headers)
        elif method.upper() == "DELETE":
            self.last_response = requests.delete(url, headers=request_headers)
        else:
            self.last_response = requests.request(method, url, json=payload, headers=request_headers)
        
        try:
            self.last_data = self.last_response.json()
        except:
            self.last_data = self.last_response.text
            
        return self
