import requests
from constants import BASE_URL, USER_NAME


class TokenManager:
    token = None

    @classmethod
    def get_token(cls):
        if cls.token and cls._is_token_valid(cls.token):
            return cls.token
        response = requests.post(f"{BASE_URL}/authorize", json={"name": USER_NAME})
        cls.token = response.json().get('token')
        return cls.token

    @classmethod
    def _is_token_valid(cls, token):
        response = requests.get(f"{BASE_URL}/authorize/{token}")
        return response.status_code == 200
