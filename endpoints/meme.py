import requests
from endpoints.base_endpoint import BaseEndpoint


class MemeEndpoint(BaseEndpoint):
    def get_all(self):
        self.logger.info("Получение списка всех мемов")
        self.last_response = requests.get(f"{self.base_url}/meme", headers=self.headers)
        response_data = self.last_response.json()
        # API возвращает объект с ключом 'data', содержащим список мемов
        self.last_data = response_data.get('data', response_data)
        return self

    def get_one(self, meme_id):
        self.logger.info(f"Получение мема по ID: {meme_id}")
        self.last_response = requests.get(f"{self.base_url}/meme/{meme_id}", headers=self.headers)
        if self.last_response.status_code == 200:
            self.last_data = self.last_response.json()
        else:
            try:
                self.last_data = self.last_response.json()
            except:
                self.last_data = self.last_response.text
        return self

    def create(self, text, url, tags, info):
        self.logger.info(f"Создание мема: {text}")
        payload = {"text": text, "url": url, "tags": tags, "info": info}
        self.last_response = requests.post(f"{self.base_url}/meme", json=payload, headers=self.headers)
        self.last_data = self.last_response.json()
        return self

    def update(self, meme_id, text, url, tags, info):
        self.logger.info(f"Обновление мема ID: {meme_id}")
        payload = {"id": meme_id, "text": text, "url": url, "tags": tags, "info": info}
        self.last_response = requests.put(f"{self.base_url}/meme/{meme_id}", json=payload, headers=self.headers)
        self.last_data = self.last_response.json()
        return self

    def delete(self, meme_id):
        self.logger.info(f"Удаление мема ID: {meme_id}")
        self.last_response = requests.delete(f"{self.base_url}/meme/{meme_id}", headers=self.headers)
        return self
    
    def create_with_custom_payload(self, payload):
        """Создание мема с кастомным payload для тестирования невалидных данных"""
        self.logger.info(f"Создание мема с кастомным payload: {payload}")
        self.last_response = requests.post(f"{self.base_url}/meme", json=payload, headers=self.headers)
        try:
            self.last_data = self.last_response.json()
        except:
            self.last_data = self.last_response.text
        return self
    
    def update_with_custom_payload(self, meme_id, payload):
        """Обновление мема с кастомным payload для тестирования невалидных данных"""
        self.logger.info(f"Обновление мема ID {meme_id} с кастомным payload: {payload}")
        self.last_response = requests.put(f"{self.base_url}/meme/{meme_id}", json=payload, headers=self.headers)
        try:
            self.last_data = self.last_response.json()
        except:
            self.last_data = self.last_response.text
        return self
    
    def get_with_invalid_token(self, invalid_token):
        """Получение мемов с невалидным токеном"""
        headers = {"Authorization": f"Bearer {invalid_token}"}
        self.logger.info(f"Попытка получить мемы с невалидным токеном: {invalid_token}")
        self.last_response = requests.get(f"{self.base_url}/meme", headers=headers)
        try:
            self.last_data = self.last_response.json()
        except:
            self.last_data = self.last_response.text
        return self

    def validate_meme(self, text=None, url=None, tags=None, info=None):
        meme = self.last_data
        if text:
            assert meme["text"] == text, f"Expected text '{text}', got '{meme['text']}'"
        if url:
            assert meme["url"] == url, f"Expected url '{url}', got '{meme['url']}'"
        if tags:
            assert meme["tags"] == tags, f"Expected tags '{tags}', got '{meme['tags']}'"
        if info:
            assert meme["info"] == info, f"Expected info '{info}', got '{meme['info']}'"
        self.logger.info("Мем прошел валидацию успешно")

    def validate_memes_list_not_empty(self):
        """Проверяет, что список мемов не пустой"""
        memes = self.last_data
        assert isinstance(memes, list), f"Expected list, got {type(memes)}"
        assert len(memes) > 0, "Expected non-empty list of memes"
        self.logger.info(f"Проверка пройдена: список содержит {len(memes)} мемов")

    def validate_meme_id(self, expected_id):
        """Проверяет ID мема"""
        meme = self.last_data
        assert meme["id"] == expected_id, f"Expected ID {expected_id}, got {meme['id']}"
        self.logger.info(f"Проверка ID пройдена: {expected_id}")

    def validate_meme_structure(self):
        """Проверяет структуру мема (наличие обязательных полей и их типов)"""
        meme = self.last_data
        assert "text" in meme and isinstance(meme["text"], str), "Field 'text' should be string"
        assert "url" in meme and isinstance(meme["url"], str), "Field 'url' should be string"
        assert "tags" in meme and isinstance(meme["tags"], list), "Field 'tags' should be list"
        assert "info" in meme and isinstance(meme["info"], dict), "Field 'info' should be dict"
        self.logger.info("Структура мема корректна")
