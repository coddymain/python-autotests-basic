
from utils.logger import logger

class BasePage:
    """Базовый класс для всех страниц с логированием."""
    def __init__(self, page):
        self.page = page

    def open_url(self, url):
        """Открытие страницы."""
        logger.info(f"🌍 Открытие страницы: {url}")
        self.page.goto(url)

    def click(self, locator):
        """Клик по элементу."""
        logger.info(f"🖱️ Клик по элементу: {locator}")
        self.page.locator(locator).click()

    def enter_text(self, locator, text):
        """Ввод текста."""
        logger.info(f"⌨️ Ввод текста '{text}' в {locator}")
        self.page.locator(locator).fill(text)

    def get_text(self, locator):
        """Получение текста элемента."""
        text = self.page.locator(locator).text_content()
        logger.info(f"📖 Получен текст из {locator}: '{text}'")
        return text