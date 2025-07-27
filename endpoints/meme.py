from endpoints.base_endpoint import BaseEndpoint


class MemeEndpoint(BaseEndpoint):
    def get_all(self):
        self.logger.info("Получение списка всех мемов")
        return self.request("get", "/meme")

    def get_one(self, meme_id):
        self.logger.info(f"Получение мема по ID: {meme_id}")
        self.request("get", f"/meme/{meme_id}")
        if self.last_response.status_code != 200:
            self.last_data = None
        return self

    def create(self, text, url, tags, info):
        self.logger.info(f"Создание мема: {text}")
        payload = {"text": text, "url": url, "tags": tags, "info": info}
        return self.request("post", "/meme", json=payload)

    def update(self, meme_id, text, url, tags, info):
        self.logger.info(f"Обновление мема ID: {meme_id}")
        payload = {"id": meme_id, "text": text, "url": url, "tags": tags, "info": info}
        return self.request("put", f"/meme/{meme_id}", json=payload)

    def delete(self, meme_id):
        self.logger.info(f"Удаление мема ID: {meme_id}")
        return self.request("delete", f"/meme/{meme_id}")

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
