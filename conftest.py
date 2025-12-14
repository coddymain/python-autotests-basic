import pytest
import allure
from playwright.sync_api import sync_playwright
from utils.logger import logger  # Импорт логгера


@pytest.fixture(scope="function")
def page():
    """Фикстура для браузера с логированием."""
    logger.info("Запуск браузера")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        yield page
        logger.info("Закрытие браузера")
        browser.close()


def pytest_exception_interact(node, report):
    """Логирование ошибок тестов."""
    if report.failed and hasattr(node, "funcargs"):
        page = node.funcargs.get("page")
        if page:
            allure.attach(
                page.screenshot(),
                name="screenshot_on_failure",
                attachment_type=allure.attachment_type.PNG,
            )
            logger.error(f"❌ Тест '{node.name}' провалился. Скриншот сохранен.")
