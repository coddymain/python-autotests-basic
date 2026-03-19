"""
Вспомогательный класс для API-запросов.
Оборачивает requests в allure-шаги и логирование.
"""
from typing import Optional

import allure
import requests

from config import Config
from utils.logger import logger


class APIHelper:
    """Помощник для выполнения HTTP-запросов с логированием."""

    def __init__(self, base_url: str = Config.API_URL):
        self.base_url = base_url

    def get(
        self,
        endpoint: str,
        params: Optional[dict] = None,
    ) -> requests.Response:
        """Выполняет GET-запрос."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        with allure.step(f"GET {url}"):
            logger.info(f"API GET: {url}, params={params}")
            response = requests.get(url, params=params)
            logger.info(f"API ответ: {response.status_code}")
            return response

    def post(
        self,
        endpoint: str,
        data: Optional[dict] = None,
        json: Optional[dict] = None,
    ) -> requests.Response:
        """Выполняет POST-запрос."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        with allure.step(f"POST {url}"):
            logger.info(f"API POST: {url}")
            response = requests.post(url, data=data, json=json)
            logger.info(f"API ответ: {response.status_code}")
            return response
