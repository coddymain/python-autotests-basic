"""
UI-тесты для сайта pizzeria.skillbox.cc.

Покрывают:
  - Применение валидного купона
  - Применение невалидных купонов
  - Авторизацию
  - Добавление товара в корзину
  - Перехват сетевых запросов (симуляция ошибки 500)
  - Оформление заказа
  - Регистрацию бонусной карты
"""
import re

import allure
import pytest
from playwright.sync_api import expect

from data.test_data import TestData
from pages.page_cart import PageCart
from utils.logger import logger


@allure.suite("UI тесты")
@allure.feature("Корзина и Оформление заказа")
class TestPizzeriaUI:

    # ── Купоны ────────────────────────────────────

    @pytest.mark.parametrize("coupon", TestData.VALID_COUPONS)
    @allure.title("Применение валидного купона: {coupon}")
    def test_apply_valid_coupon(self, cart_page: PageCart, coupon: str) -> None:
        """Проверяем, что при применении действующего купона появляется сообщение об успехе."""
        cart_page.open()
        cart_page.clear_cart()
        cart_page.add_pizza_to_cart()
        cart_page.go_to_cart()
        cart_page.apply_coupon(coupon)

        success = cart_page.page.locator(".woocommerce-message")
        expect(success).to_be_visible(timeout=10000)

    @pytest.mark.parametrize("coupon", TestData.INVALID_COUPONS)
    @allure.title("Применение невалидного купона: {coupon}")
    def test_apply_invalid_coupon(self, cart_page: PageCart, coupon: str) -> None:
        """Проверяем, что при вводе несуществующего купона появляется ошибка."""
        cart_page.open()
        cart_page.clear_cart()
        cart_page.add_pizza_to_cart()
        cart_page.go_to_cart()

        error_msg = cart_page.apply_invalid_coupon(coupon)
        error_lower = error_msg.lower()
        assert any(
            word in error_lower
            for word in ["неверный", "не существует", "invalid", "does not exist"]
        ), f"Неожиданное сообщение: {error_msg}"

    # ── Авторизация ───────────────────────────────

    @allure.title("Вход в аккаунт")
    def test_login(self, cart_page: PageCart) -> None:
        """Проверяем, что можно войти и увидеть приветствие."""
        cart_page.open()
        cart_page.go_to_account()
        cart_page.login()
        cart_page.verify_logged_in()

    # ── Корзина ───────────────────────────────────

    @allure.title("Добавление товара в корзину")
    def test_add_pizza_to_cart(self, cart_page: PageCart) -> None:
        """Проверяем, что при добавлении пиццы она появляется в корзине."""
        cart_page.open()
        cart_page.clear_cart()
        cart_page.add_pizza_to_cart()
        cart_page.go_to_cart()

        qty = int(cart_page.get_cart_quantity())
        assert qty >= 1, f"Ожидали >= 1 товар, получили {qty}"

    # ── Перехват сети ─────────────────────────────

    @allure.title("Симуляция ошибки 500 при применении купона")
    def test_block_network_request(self, cart_page: PageCart) -> None:
        """Проверяем, что при перехвате запроса купона приложение не падает."""
        cart_page.open()
        cart_page.add_pizza_to_cart()
        cart_page.go_to_cart()
        cart_page.simulate_coupon_error("ANY_CODE")
        logger.info("✅ Симуляция ошибки 500 выполнена")

    # ── Оформление заказа ─────────────────────────

    @allure.title("Оформление заказа")
    def test_checkout(self, cart_page: PageCart) -> None:
        """Проверяем полный цикл: логин → товар в корзину → оформление."""
        cart_page.open()
        cart_page.go_to_account()
        cart_page.login()

        cart_page.clear_cart()
        cart_page.add_pizza_to_cart()
        cart_page.go_to_cart()
        cart_page.checkout(**TestData.DEFAULT_USER)
        cart_page.verify_order_received()

    # ── Бонусная программа ────────────────────────

    @allure.title("Регистрация бонусной карты")
    def test_bonus_registration(self, cart_page: PageCart) -> None:
        """Проверяем, что можно зарегистрировать бонусную карту."""
        cart_page.open()
        cart_page.register_bonus_card(**TestData.BONUS_USER)
        cart_page.verify_bonus_success()
