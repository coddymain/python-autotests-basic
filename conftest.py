"""
Конфигурация pytest и фикстуры.

Содержит:
  - page: фикстура запуска Playwright-браузера
  - cart_page: фикстура PageCart
  - pytest_runtest_makereport: скриншоты при падении тестов
"""
import os

import allure
import pytest
from playwright.sync_api import sync_playwright, Page

from pages.page_cart import PageCart
from utils.logger import logger


@pytest.fixture(scope="function")
def page():
    """Запускает браузер и отдаёт страницу. Закрывает после теста."""
    logger.info("🚀 Запуск браузера")
    with sync_playwright() as pw:
        headless = os.getenv("HEADLESS", "true").lower() == "true"
        browser = pw.chromium.launch(headless=headless)
        context = browser.new_context()
        yield context.new_page()
        logger.info("🛑 Закрытие браузера")
        browser.close()


@pytest.fixture(scope="function")
def cart_page(page: Page) -> PageCart:
    """Создаёт и возвращает PageCart для теста."""
    return PageCart(page)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Делает скриншот при падении теста и прикрепляет к allure-отчёту."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        if "page" in item.fixturenames:
            page = item.funcargs["page"]
            allure.attach(
                page.screenshot(),
                name="screenshot_on_failure",
                attachment_type=allure.attachment_type.PNG,
            )
            logger.error(f"❌ Тест '{item.name}' упал. Скриншот прикреплён.")
