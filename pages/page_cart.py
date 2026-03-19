"""
Page Object для страниц: Главная, Корзина, Оформление заказа, Аккаунт, Бонусная программа.
Все действия с сайтом pizzeria.skillbox.cc собраны здесь.
"""
import re
from typing import Optional

import allure
from playwright.sync_api import Page, Route, expect

from config import Config
from pages.base_page import BasePage
from utils.logger import logger


class PageCart(BasePage):
    """Page Object для работы с корзиной и оформлением заказа."""

    # ──────────────────────────────────────────────
    # Локаторы — CSS-селекторы элементов на сайте
    # ──────────────────────────────────────────────
    class Locators:
        # Авторизация (страница /my-account/)
        LOGIN_INPUT = "#username"
        PASSWORD_INPUT = "#password"
        LOGIN_BUTTON = 'button[name="login"]'
        ACCOUNT_CONTENT = ".woocommerce-MyAccount-content"

        # Корзина
        ADD_TO_CART_BUTTON = 'a[data-product_id="425"]'
        CART_TABLE = ".shop_table.cart"
        CART_EMPTY = ".cart-empty"
        QUANTITY_INPUT = 'input.qty'
        REMOVE_ITEM = "a.remove"
        UPDATE_CART = 'button[name="update_cart"]'
        CART_TOTAL = ".order-total .amount"
        CART_SUBTOTAL = ".cart-subtotal .amount"

        # Купоны
        COUPON_INPUT = "#coupon_code"
        APPLY_COUPON = 'button[name="apply_coupon"]'
        COUPON_SUCCESS = ".woocommerce-message"
        COUPON_ERROR = ".woocommerce-error"

        # Оформление заказа (страница /checkout/)
        FIRST_NAME = "#billing_first_name"
        LAST_NAME = "#billing_last_name"
        COUNTRY = "#billing_country"
        ADDRESS = "#billing_address_1"
        CITY = "#billing_city"
        STATE = "#billing_state"
        POSTCODE = "#billing_postcode"
        PHONE = "#billing_phone"
        PAYMENT_COD = "#payment_method_cod"
        TERMS = "#terms"
        PLACE_ORDER = "#place_order"
        ORDER_RECEIVED = "p.woocommerce-thankyou-order-received"

        # Бонусная программа (страница /bonus/)
        BONUS_USERNAME = "#bonus_username"
        BONUS_PHONE = "#bonus_phone"
        BONUS_SUBMIT = "button.woocommerce-form-register__submit"
        BONUS_SUCCESS = ".woocommerce-message"

    # ──────────────────────────────────────────────
    # Инициализация
    # ──────────────────────────────────────────────
    def __init__(self, page: Page):
        super().__init__(page)
        self._price_before: Optional[float] = None

    # ──────────────────────────────────────────────
    # Навигация
    # ──────────────────────────────────────────────
    def open(self) -> None:
        """Открывает главную страницу."""
        with allure.step("Открыть главную страницу"):
            self.open_url(Config.BASE_URL)

    # ──────────────────────────────────────────────
    # Корзина
    # ──────────────────────────────────────────────
    def clear_cart(self) -> None:
        """Полностью очищает корзину."""
        with allure.step("Очистить корзину"):
            self.page.goto(f"{Config.BASE_URL}/cart/")
            self.page.wait_for_load_state("networkidle")

            while self.page.locator(self.Locators.REMOVE_ITEM).count() > 0:
                self.page.locator(self.Locators.REMOVE_ITEM).first.click()
                self.page.wait_for_load_state("networkidle")
                self.page.wait_for_timeout(500)

    def add_pizza_to_cart(self) -> None:
        """Добавляет «Пиццу 4 в 1» в корзину через прямой URL (самый надёжный способ)."""
        with allure.step("Добавить пиццу в корзину"):
            self.page.goto(f"{Config.BASE_URL}/?add-to-cart=425")
            self.page.wait_for_load_state("networkidle")

    def go_to_cart(self) -> None:
        """Переходит на страницу корзины."""
        with allure.step("Перейти в корзину"):
            self.page.goto(f"{Config.BASE_URL}/cart/")
            self.page.wait_for_selector(
                f"{self.Locators.CART_TABLE}, {self.Locators.CART_EMPTY}",
                timeout=15000,
            )

    def get_cart_quantity(self) -> str:
        """Возвращает количество первого товара в корзине."""
        locator = self.page.locator(self.Locators.QUANTITY_INPUT).first
        locator.wait_for(state="visible", timeout=10000)
        return locator.input_value()

    def get_total_price(self) -> float:
        """Возвращает итоговую цену как число."""
        self.page.wait_for_timeout(1000)
        price_text = self.page.locator(self.Locators.CART_SUBTOTAL).first.text_content() or "0"
        clean = price_text.replace("₽", "").replace(" ", "").replace(",", ".").replace("\xa0", "").strip()
        return float(clean)

    # ──────────────────────────────────────────────
    # Купоны
    # ──────────────────────────────────────────────
    def apply_coupon(self, code: str) -> None:
        """Применяет купон."""
        with allure.step(f"Применить купон: {code}"):
            self.page.locator(self.Locators.COUPON_INPUT).fill(code)
            self.page.locator(self.Locators.APPLY_COUPON).click()
            # Ждём появления любого сообщения
            self.page.wait_for_selector(
                f"{self.Locators.COUPON_SUCCESS}, {self.Locators.COUPON_ERROR}",
                timeout=10000,
            )

    def apply_invalid_coupon(self, code: str) -> str:
        """Применяет невалидный купон и возвращает текст ошибки."""
        with allure.step(f"Применить невалидный купон: {code}"):
            self.page.locator(self.Locators.COUPON_INPUT).fill(code)
            self.page.locator(self.Locators.APPLY_COUPON).click()
            error = self.page.locator(self.Locators.COUPON_ERROR)
            expect(error).to_be_visible(timeout=10000)
            return error.text_content() or ""

    def simulate_coupon_error(self, code: str) -> None:
        """Симулирует ошибку 500 при применении купона (перехват сети)."""
        with allure.step(f"Симуляция ошибки 500 для купона: {code}"):
            def block(route: Route) -> None:
                route.fulfill(status=500, body="Internal Server Error")

            self.page.route(re.compile(r"wc-ajax=apply_coupon"), block)
            self.page.locator(self.Locators.COUPON_INPUT).fill(code)
            self.page.locator(self.Locators.APPLY_COUPON).click()

    # ──────────────────────────────────────────────
    # Авторизация
    # ──────────────────────────────────────────────
    def go_to_account(self) -> None:
        """Переходит на страницу «Мой аккаунт»."""
        with allure.step("Перейти в Мой аккаунт"):
            self.page.goto(f"{Config.BASE_URL}/my-account/")
            self.page.wait_for_load_state("networkidle")

    def login(
        self,
        username: str = Config.USER_LOGIN,
        password: str = Config.USER_PASSWORD,
    ) -> None:
        """Выполняет вход. Если уже залогинен — пропускает."""
        # Убеждаемся что мы на странице аккаунта
        if "/my-account" not in self.page.url:
            self.go_to_account()

        # Если уже залогинены — выходим
        if self.page.locator(self.Locators.ACCOUNT_CONTENT).count() > 0:
            content = self.page.locator(self.Locators.ACCOUNT_CONTENT).text_content() or ""
            if username in content:
                logger.info(f"✅ Уже залогинен как {username}")
                return

        with allure.step(f"Войти как {username}"):
            self.page.locator(self.Locators.LOGIN_INPUT).fill(username)
            self.page.locator(self.Locators.PASSWORD_INPUT).fill(password)
            self.page.locator(self.Locators.LOGIN_BUTTON).click()
            self.page.wait_for_load_state("networkidle")

    def verify_logged_in(self, username: str = Config.USER_LOGIN) -> None:
        """Проверяет, что пользователь залогинен."""
        with allure.step(f"Проверить что {username} залогинен"):
            expect(self.page.locator(self.Locators.ACCOUNT_CONTENT)).to_be_visible(timeout=10000)
            expect(self.page.locator("body")).to_contain_text(username)

    # ──────────────────────────────────────────────
    # Оформление заказа
    # ──────────────────────────────────────────────
    def go_to_checkout(self) -> None:
        """Переходит на страницу оформления заказа."""
        with allure.step("Перейти к оформлению"):
            self.page.goto(f"{Config.BASE_URL}/checkout/")
            self.page.wait_for_selector(self.Locators.FIRST_NAME, timeout=15000)

    def checkout(
        self,
        name: str,
        surname: str,
        address: str,
        city: str,
        state: str,
        postcode: str,
        phone: str,
    ) -> None:
        """Заполняет форму заказа и нажимает «Оформить заказ»."""
        self.go_to_checkout()

        with allure.step("Заполнить данные и оформить заказ"):
            self.page.locator(self.Locators.FIRST_NAME).fill(name)
            self.page.locator(self.Locators.LAST_NAME).fill(surname)
            self.page.locator(self.Locators.COUNTRY).select_option("RU")
            self.page.locator(self.Locators.ADDRESS).fill(address)
            self.page.locator(self.Locators.CITY).fill(city)
            self.page.locator(self.Locators.STATE).fill(state)
            self.page.locator(self.Locators.POSTCODE).fill(postcode)
            self.page.locator(self.Locators.PHONE).fill(phone)

            self.page.locator(self.Locators.PAYMENT_COD).check()
            self.page.locator(self.Locators.TERMS).check()
            self.page.wait_for_timeout(500)
            self.page.locator(self.Locators.PLACE_ORDER).click()

    def verify_order_received(self) -> None:
        """Проверяет что заказ успешно принят."""
        with allure.step("Проверить подтверждение заказа"):
            msg = self.page.locator(self.Locators.ORDER_RECEIVED)
            expect(msg).to_be_visible(timeout=30000)

    # ──────────────────────────────────────────────
    # Бонусная программа
    # ──────────────────────────────────────────────
    def register_bonus_card(self, username: str, phone: str) -> None:
        """Регистрирует бонусную карту."""
        with allure.step(f"Оформить бонусную карту для {username}"):
            self.page.goto(f"{Config.BASE_URL}/bonus/")
            self.page.wait_for_selector(self.Locators.BONUS_USERNAME, timeout=15000)
            self.page.locator(self.Locators.BONUS_USERNAME).fill(username)
            self.page.locator(self.Locators.BONUS_PHONE).fill(phone)
            self.page.locator(self.Locators.BONUS_SUBMIT).click()

    def verify_bonus_success(self) -> None:
        """Проверяет успешную регистрацию бонусной карты."""
        with allure.step("Проверить успешную выдачу бонусной карты"):
            # После оформления форма заменяется на <h3>Ваша карта оформлена!</h3>
            msg = self.page.get_by_text("Ваша карта оформлена")
            expect(msg).to_be_visible(timeout=15000)