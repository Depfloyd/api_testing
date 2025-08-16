import requests
from constants import BASE_URL
from utils.logger import setup_logger


class UnauthorizedMemeEndpoint:
    """Класс для тестирования endpoints без авторизации"""
    
    def __init__(self):
        self.base_url = BASE_URL
        self.last_response = None
        self.last_data = None
        self.logger = setup_logger(self.__class__.__name__)

    def get_all(self, headers=None):
        """Получение списка всех мемов без авторизации"""
        auth_info = "с невалидным/пустым токеном" if headers else "без токена авторизации"
        self.logger.info(f"Получение списка всех мемов {auth_info}")
        self.last_response = requests.get(f"{self.base_url}/meme", headers=headers or {})
        try:
            self.last_data = self.last_response.json()
        except:
            self.last_data = self.last_response.text
        return self

    def get_one(self, meme_id, headers=None):
        """Получение мема по ID без авторизации"""
        auth_info = "с невалидным/пустым токеном" if headers else "без токена авторизации"
        self.logger.info(f"Получение мема по ID {meme_id} {auth_info}")
        self.last_response = requests.get(f"{self.base_url}/meme/{meme_id}", headers=headers or {})
        try:
            self.last_data = self.last_response.json()
        except:
            self.last_data = self.last_response.text
        return self

    def create(self, text, url, tags, info, headers=None):
        """Создание мема без авторизации"""
        auth_info = "с невалидным/пустым токеном" if headers else "без токена авторизации"
        self.logger.info(f"Создание мема '{text}' {auth_info}")
        payload = {"text": text, "url": url, "tags": tags, "info": info}
        self.last_response = requests.post(f"{self.base_url}/meme", json=payload, headers=headers or {})
        try:
            self.last_data = self.last_response.json()
        except:
            self.last_data = self.last_response.text
        return self

    def update(self, meme_id, text, url, tags, info, headers=None):
        """Обновление мема без авторизации"""
        auth_info = "с невалидным/пустым токеном" if headers else "без токена авторизации"
        self.logger.info(f"Обновление мема ID {meme_id} {auth_info}")
        payload = {"id": meme_id, "text": text, "url": url, "tags": tags, "info": info}
        self.last_response = requests.put(f"{self.base_url}/meme/{meme_id}", json=payload, headers=headers or {})
        try:
            self.last_data = self.last_response.json()
        except:
            self.last_data = self.last_response.text
        return self

    def delete(self, meme_id, headers=None):
        """Удаление мема без авторизации"""
        auth_info = "с невалидным/пустым токеном" if headers else "без токена авторизации"
        self.logger.info(f"Удаление мема ID {meme_id} {auth_info}")
        self.last_response = requests.delete(f"{self.base_url}/meme/{meme_id}", headers=headers or {})
        try:
            self.last_data = self.last_response.json()
        except:
            self.last_data = self.last_response.text
        return self

    def check_status_code(self, expected_code):
        """Проверка статус кода ответа"""
        actual_code = self.last_response.status_code
        assert actual_code == expected_code, (
            f"Expected status code {expected_code}, got {actual_code}"
        )
        self.logger.info(f"Проверен статус код: {actual_code} (ожидаемый: {expected_code})")

    def check_status_code_in_range(self, expected_codes):
        """Проверяет, что статус код находится в списке ожидаемых кодов"""
        actual_code = self.last_response.status_code
        assert actual_code in expected_codes, (
            f"Expected status code in {expected_codes}, got {actual_code}"
        )
        self.logger.info(f"Проверен статус код: {actual_code} (ожидаемый один из: {expected_codes})")

    def validate_unauthorized_error(self):
        """Проверяет, что в ответе есть сообщение об ошибке авторизации"""
        try:
            error_data = self.last_response.json()
            assert "error" in error_data or "message" in error_data
            self.logger.info(f"Проверена ошибка авторизации в JSON ответе: {error_data}")
        except:
            # Если ответ не JSON, проверяем текст
            assert "Unauthorized" in self.last_response.text or "401" in self.last_response.text
            self.logger.info(f"Проверена ошибка авторизации в текстовом ответе: {self.last_response.text[:100]}...")
