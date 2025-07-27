import requests
from endpoints.base_endpoint import BaseEndpoint

class AuthorizeEndpoint(BaseEndpoint):

    def authorize(self, name):
        self.logger.info(f"Авторизация пользователя: '{name}'")
        self.last_response = requests.post(
            f"{self.base_url}/authorize", json={"name": name}
        )
        self.last_data = self.last_response.json()
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
