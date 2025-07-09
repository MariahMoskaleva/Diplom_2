import requests

from utils import config


class ApiClient:

    def __init__(self):
        self.base_url = config.BASE_URL
        self.default_headers = config.DEFAULT_HEADERS

    def _full_url(self, path):
        return f"{self.base_url}{path}"

    def post(self, path: str, json=None, headers=None, **kwargs):
        url = self._full_url(path)
        response = requests.post(url=url, json=json, headers=headers)
        return response

    def get(self, path: str, headers=None, **kwargs):
        url = self._full_url(path)
        response = requests.get(url=url, headers=headers)
        return response

    def put(self, path: str, json=None, headers=None, **kwargs):
        url = self._full_url(path)
        response = requests.put(url=url, json=json, headers=headers)
        return response

    def delete(self, path: str, headers=None, **kwargs):
        url = self._full_url(path)
        response = requests.delete(url=url, headers=headers)
        return response

    def patch(self, path: str, headers=None, **kwargs):
        url = self._full_url(path)
        response = requests.patch(url=url, headers=headers)
        return response
