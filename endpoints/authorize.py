import requests
from endpoints.base_endpoint import BaseEndpoint


class AuthorizeEndpoint(BaseEndpoint):

    def authorize(self, name):
        self.last_response = requests.post(
            f"{self.base_url}/authorize", json={"name": name}
        )
        self.last_data = self.last_response.json()
        return self

    def validate_token(self):
        assert "token" in self.last_data, "Token not found in response"
