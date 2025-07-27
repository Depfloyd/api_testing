from endpoints.base_endpoint import BaseEndpoint


class MemeEndpoint(BaseEndpoint):
    def get_all(self):
        self.last_response = requests.get(f"{self.base_url}/meme", headers=self.headers)
        self.last_data = self.last_response.json()
        return self

    def get_one(self, meme_id):
        self.last_response = requests.get(f"{self.base_url}/meme/{meme_id}", headers=self.headers)
        if self.last_response.status_code == 200:
            self.last_data = self.last_response.json()
        else:
            self.last_data = None
        return self

    def create(self, text, url, tags, info):
        payload = {"text": text, "url": url, "tags": tags, "info": info}
        self.last_response = requests.post(f"{self.base_url}/meme", json=payload, headers=self.headers)
        self.last_data = self.last_response.json()
        return self

    def update(self, meme_id, text, url, tags, info):
        payload = {"id": meme_id, "text": text, "url": url, "tags": tags, "info": info}
        self.last_response = requests.put(f"{self.base_url}/meme/{meme_id}", json=payload, headers=self.headers)
        self.last_data = self.last_response.json()
        return self

    def delete(self, meme_id):
        self.last_response = requests.delete(f"{self.base_url}/meme/{meme_id}", headers=self.headers)
        return self

    def validate_meme(self, text=None, url=None, tags=None, info=None):
        meme = self.last_data
        if text:
            assert meme["text"] == text, f"Expected text {text}, got {meme['text']}"
        if url:
            assert meme["url"] == url, f"Expected url {url}, got {meme['url']}"
        if tags:
            assert meme["tags"] == tags, f"Expected tags {tags}, got {meme['tags']}"
        if info:
            assert meme["info"] == info, f"Expected info {info}, got {meme['info']}"
