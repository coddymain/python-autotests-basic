"""
Базовый класс для всех Page Object.
Содержит общие методы, которые используются на любой странице.
"""
from utils.logger import logger
from playwright.sync_api import Page


class BasePage:
    """Базовый класс для Page Objects."""

    def __init__(self, page: Page):
        self.page = page

    def open_url(self, url: str) -> None:
        """Открывает указанный URL."""
        logger.info(f"🌍 Открываю: {url}")
        self.page.goto(url)
        self.page.wait_for_load_state("domcontentloaded")

    def get_text(self, selector: str) -> str:
        """Возвращает текст элемента по селектору."""
        return self.page.locator(selector).text_content() or ""