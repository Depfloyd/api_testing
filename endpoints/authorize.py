import requests
from endpoints.base_endpoint import BaseEndpoint

class AuthorizeEndpoint(BaseEndpoint):

    def post_authorize(self, name):
        self.logger.info(f"Авторизация пользователя: '{name}'")
        self.last_response = requests.post(
            f"{self.base_url}/authorize", json={"name": name}
        )
        try:
            self.last_data = self.last_response.json()
        except Exception:
            self.last_data = self.last_response.text
        return self

    def validate_token(self):
        assert "token" in self.last_data, "Token not found in response"
        token = self.last_data['token']
        self.logger.info(f"Получен токен: {token}")
        return self

    def check_token(self, token):
        self.logger.info(f"Проверка валидности токена: {token}")
        self.last_response = requests.get(f"{self.base_url}/authorize/{token}")
        return self

    def validate_empty_body_error(self):
        """Проверяет ошибку при отправке пустого тела запроса"""
        self.validate_error_response(["Bad Request", "Invalid", "error", "message"])
