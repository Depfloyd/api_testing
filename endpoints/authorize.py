from endpoints.base_endpoint import BaseEndpoint

class AuthorizeEndpoint(BaseEndpoint):

    def authorize(self, name):
        self.logger.info(f"Авторизация пользователя: '{name}'")
        return self.request("post", "/authorize", json={"name": name})

    def validate_token(self):
        assert "token" in self.last_data, "Token not found in response"
        token = self.last_data['token']
        self.logger.info(f"Получен токен: {token}")
        return self

    def check_token(self, token):
        self.logger.info(f"Проверка валидности токена: {token}")
        return self.request("get", f"/authorize/{token}")
