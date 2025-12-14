import time
import allure
from pages.base_page import BasePage
from utils.logger import logger
import re
from playwright.sync_api import Page, expect, Route

class PageCart(BasePage):
    def __init__(self, page: Page):
        self.page = page


    URL = 'https://pizzeria.skillbox.cc/'
    CART_LOCTOR = '(//a/text()[. ="Корзина"])[1]' # Корзина
    DESCRIPTION_TAB = "//h1[@class='product_title entry-title']" # описние
    COUTN_CART ='#quantity_67b8ac6f731fd'  # Счетчик карзины
    REFRESH_CART = "//button[contains(text(),'Обновить корзину')]" # Кнопка обновить корзину
    CHEESE_BORT_LOCATOR = "//p[contains(text(),'Сырный борт')]"


    # АВТОРИЗНЦИЯ
    # Открытие главной страницы
    def open(self):
        self.page.goto(self.URL)


    # Перейти в меню оформление заказа
    def menu_make_order(self):
        self.page.locator("#menu-item-31").get_by_role("link", name="Оформление заказа").click()


    # Пеерйти в меню мой аккаунт
    def menu_my_account(self):
       self.page.locator("#menu-item-30").get_by_role("link", name="Мой аккаунт").click()
       self.page.wait_for_timeout(timeout=120)
   # Заполниить поле логин
    def fill_imput_login(self):
       self.page.get_by_role("textbox", name="Имя пользователя или почта *").fill("erastov")
    # Заполниить поле пароль
    def fill_input_password(self):
       self.page.get_by_role("textbox", name="Пароль *").fill("12345")
    # Кликнуть по кнопке войти
    def clik_button_login(self):
       self.page.get_by_role("button", name="Войти").click()
    # Проверить что бы успешно залогились
    def checking_have_to_login(self):
       expect(self.page.locator("#post-22")).to_contain_text("Привет erastov (Выйти)")

        # Открытие глванойстраницы
    def open(self):
        self.page.goto(self.URL)
    def add_pizza_to_cart(self):
        # Клик по кнопке "Добавить пиццу «4 в 1» в корзину"
        self.page.get_by_role("link", name="Add “Пицца \"4 в 1\"” to your").click()

    def in_to_cart(self):
        self.page.locator("#menu-item-29").get_by_role("link", name="Корзина").click()
        # Обновить корзину
        self.page.reload()
    def checking_cart_is_not_empty(self):
        # Проверка, что значение в поле количества равно "1" (пицца добавлена в корзину)
        expect(self.page.get_by_role("spinbutton", name="Пицца \"4 в 1\" quantity")).to_have_value('1')
    # Кликаем по изображению пиццы
    def click_pizza_img(self):
# Кликнуть по пицце (с явным ожиданием)
        pizza_link = self.page.get_by_role("link", name="Пицца «4 в 1»", exact=True)
        pizza_link.wait_for()  # Ждем, пока ссылка появится
        pizza_link.click()

    def checking_description_is_that_pizza(self):
        expect(self.page.locator("#product-425")).to_contain_text("Пицца «4 в 1»")


    def increase_velue_in_cart(self): # Увеличить количество корзины.
       self.page.get_by_role("spinbutton", name="Пицца \"4 в 1\" quantity").fill("2")

    def refresh_cart(self):
        self.page.get_by_role("button", name="Обновить корзину").click()


    def checking_cart_is_increase(self):
        expect(self.page.get_by_role("spinbutton", name='Пицца "4 в 1" quantity')).to_have_value("2")

    # Выбрать борт пицы из возможных
    def choose_chees_bort_pizza(self):
        self.page.get_by_label("Выбор борта для пиццы *").select_option("55.00")

        # Нажать кнопку добавить пиццу в корзину
    def add_pizza_with_chees_bort(self):
        self.page.get_by_role("button", name="В корзину").click()

    def clck_autorisation(self):
        self.page.get_by_role("link", name="Авторизуйтесь").click()

    def click_button_login(self):
       self.page.get_by_role("button", name="Войти").click()

    def fill_all_feald(self):
        self.page.get_by_role("textbox", name="Имя *").fill("Иван")
        self.page.get_by_role("textbox", name="Фамилия *").fill("Иванов")
        self.page.get_by_role("textbox", name="Russia").click()
        self.page.get_by_role("option", name="Russia").click()
        self.page.get_by_role("textbox", name="Адрес *").fill("ул. Ивановская д.1")
        self.page.get_by_role("textbox", name="Город / Населенный пункт *").fill("Иваново")
        self.page.get_by_role("textbox", name="Область *").fill("Ивановская")
        self.page.get_by_role("textbox", name="Почтовый индекс *").fill("134506")
        self.page.get_by_role("textbox", name="Телефон *").fill("+79116118292")
        self.page.get_by_role("textbox", name="Дата заказа (дополнительно)").fill("2025-03-19")
        self.page.get_by_role("radio", name="Оплата при доставке").check()
        self.page.get_by_role("checkbox", name="I have read and agree to the").check()
    def click_make_order(self):
        self.page.get_by_role("button", name="Оформить заказ").click()
    def checking_maged_order(self):
        expect(self.page.locator("#post-24")).to_contain_text("Заказ получен")


        # Используем промокод
    def fill_kupon_GIVEMEHALYAVA(self):

        self.page.get_by_role("textbox", name="Купон:").fill("GIVEMEHALYAVA")
    def click_apply_kupon(self):
        self.page.get_by_role("button", name="Применить купон").click()
        self.page.reload()
        self.total_price = self.page.locator("//td[@data-title='Сумма']")

        self.total_price = self.total_price.text_content().replace("₽", "").replace(",", ".")
        self.total_price = float(self.total_price)
    def checking_kuppon_is_good(self):
        self.discounted_price = (self.total_price * 0.9)
        with allure.step("Проверяем применение промокода"):
            logger.info(f"Сумма до применения купона {self.total_price} сумма после приенения купона {self.discounted_price}")
        assert self.total_price * 0.9 == self.discounted_price, "Скидка не применена!"



    def fill_facke_kupon_DC120(self):
        self.page.get_by_role("textbox", name="Купон:").fill("DC120")
        self.page.reload()

    def checking_fake_kuppon_is_no_good(self):
        self.price = self.page.locator(("(//td[@data-title='Общая стоимость'])[1]"))
        self.total_price = self.page.locator("//td[@data-title='Сумма']")

        self.price = self.price.text_content().replace("₽", "").replace(",", ".")
        self.price = float(self.price)
        self.total_price = self.total_price.text_content().replace("₽", "").replace(",", ".")
        self.total_price = float(self.total_price)

        with allure.step("Проверяем применение промокода"):
            logger.info(f"Сумма до применения купона {self.total_price} сумма после приенения купона {self.price}")
        assert self.total_price == self.price, "Скидка не применена!"




    def block_request_kupon(page: Page) -> None:
        page.goto("https://pizzeria.skillbox.cc/")
        page.get_by_role("link", name="Add “Пицца \"4 в 1\"” to your").click()
        page.wait_for_timeout(timeout=2000)

        page.locator("#menu-item-31").get_by_role("link", name="Оформление заказа").click()
        time.sleep(1)
    def autorisetion_get_order(self: Page) -> None:
        self.page.get_by_role("link", name="Авторизуйтесь").click()
        self.page.get_by_role("textbox", name="Имя пользователя или почта *").fill("erastov")

        self.page.get_by_role("textbox", name="Пароль *").fill("12345")
        self.page.get_by_role("button", name="Войти").click()

    def sent_kupon_GIVEMEHALYAVA__and_block_rquest(self: Page) -> None:
        self.page.wait_for_timeout(timeout=2000)
        self.page.wait_for_selector("//a[@class='showcoupon']").click()
        self.page.wait_for_selector("#coupon_code").fill("GIVEMEHALYAVA")

        # Перехватить и заблокировать запрос с купоном (вернуть ошибку 500)
        def block_request(route: Route):
            route.fulfill(status=500, body="Internal Server Error")

            self.page.route(re.compile(r'apply_coupon'), block_request)
            # Применить купон
            self.page.get_by_role("button", name="Применить купон").click()
        # Проверка, что купон не применился, сумма не изменилась
    def fill_data_and_check(self: Page) -> None:
        self.cart_price = self.page.locator("//a[@class='cart-contents wcmenucart-contents']")
        self.total_price = self.page.locator("(//span[@class='woocommerce-Price-amount amount'])[3]")
        # Форматируем и переводим в формат float
        self.cart_price = self.cart_price.text_content().replace("₽", "").replace(",", ".").replace('[', '').replace(']', '')
        self.cart_price = float(self.cart_price)
        self.total_price = self.total_price.text_content().replace("₽", "").replace(",", ".")
        self.total_price = float(self.total_price)

        with allure.step("Проверяем применение промокода"):
            logger.info(f"Сумма до применения купона {self.total_price} сумма после приенения купона {self.cart_price}")
        assert self.total_price ==self. cart_price, "Скидка не применена!"

        self.page.get_by_role("textbox", name="Имя *").fill("Иван")
        self.page.get_by_role("textbox", name="Фамилия *").fill("Иванов")
        self.page.get_by_role("textbox", name="Russia").click()
        self.page.get_by_role("option", name="Russia").click()
        self.page.get_by_role("textbox", name="Адрес *").fill("ул. Ивановская д.1")
        self.page.get_by_role("textbox", name="Город / Населенный пункт *").fill("Иваново")
        self.page.get_by_role("textbox", name="Область *").fill("Ивановская")
        self.page.get_by_role("textbox", name="Почтовый индекс *").fill("134506")
        self.page.get_by_role("textbox", name="Телефон *").fill("+79116118292")
        self.page.get_by_role("textbox", name="Дата заказа (дополнительно)").fill("2025-02-19")
        self.page.get_by_role("radio", name="Оплата при доставке").check()
        self.page.get_by_role("checkbox", name="I have read and agree to the").check()

        self.page.get_by_role("button", name="Оформить заказ").click()
        expect(self.page.locator("#post-24")).to_contain_text("Заказ получен")

    def registration_bonus_program(self: Page) -> None:
        self.page.wait_for_timeout(timeout=2000)
    def fill_data_bonus(self: Page) -> None:
        self.page.get_by_role('link', name='Бонусная программа').nth(1).click()
        self.page.wait_for_selector('#bonus_username').fill('test')
        self.page.wait_for_selector('#bonus_phone').fill('+71234567890')
    def click_button_get_bonus(self: Page) -> None:
        self.page.get_by_role('button', name='Оформить карту').click()
        self.page.on('dialog', lambda dialog: dialog.accept())
    def check_registration_bonus_program(self: Page) -> None:
        self.result = self.page.wait_for_selector("//h3[contains(text(),'Ваша карта оформлена')]").text_content()
        assert 'Ваша карта оформлена!' == self.result, 'Бонус не оформлен'