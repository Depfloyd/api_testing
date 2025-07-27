import requests
from constants import BASE_URL, USER_NAME


class TokenManager:
    token = None

    @classmethod
    def get_token(cls):
        if cls.token and cls._is_token_valid(cls.token):
            return cls.token
        response = requests.post(
            f"{BASE_URL}/authorize", json={"name": USER_NAME}
        )
        if response.status_code != 200:
            raise Exception(
                f"Failed to obtain token: status {response.status_code}"
            )

        data = response.json()
        if "token" not in data:
            raise Exception("Token not found in response")

        cls.token = data.get("token")
        return cls.token

    @classmethod
    def _is_token_valid(cls, token):
        response = requests.get(f"{BASE_URL}/authorize/{token}")
        return response.status_code == 200
