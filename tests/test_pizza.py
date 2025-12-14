import time
from pizzeria_tests.pages.page_cart import PageCart
from playwright.sync_api import Page, expect
import allure
import logging

# Настройка логгера
logging.basicConfig(
    level=logging.INFO,  # Уровень логирования
    format="%(asctime)s - %(levelname)s - %(message)s",  # Формат сообщений
    handlers=[logging.StreamHandler()]
)  # Вывод в консоль
logger = logging.getLogger(__name__)


def test_log_in(page: Page) -> None:

    with allure.step("Открыть главную страницу"):
        page.cart = PageCart(page)
        page.cart.open()
        logger.info("Главная страница открыта")

    with allure.step("Перейти в меню 'Мой аккаунт'"):
        page.cart.menu_my_account()
        logger.info("Меню 'Мой аккаунт' открыто")

    with allure.step("Заполнить поле логина"):
        page.cart.fill_imput_login()
        logger.info("Поле логина заполнено")

    with allure.step("Заполнить поле пароля"):
        page.cart.fill_input_password()
        logger.info("Поле пароля заполнено")

    with allure.step("Нажать кнопку 'Войти'"):
        page.cart.clik_button_login()
        logger.info("Кнопка 'Войти' нажата")

    with allure.step("Проверить успешный вход"):
        page.cart.checking_have_to_login()
        logger.info("Вход выполнен успешно")


def test_add_pizza_cart(page: Page) -> None:

    with allure.step("Открыть главную страницу"):
        page.cart = PageCart(page)
        page.cart.open()
        logger.info("Главная страница открыта")

    with allure.step("Добавить пиццу в корзину"):
        page.cart.add_pizza_to_cart()
        logger.info("Пицца добавлена в корзину")

    with allure.step("Перейти в корзину"):
        page.cart.in_to_cart()
        logger.info("Переход в корзину выполнен")

    with allure.step("Проверить, что корзина не пуста"):
        page.cart.checking_cart_is_not_empty()
        logger.info("Корзина не пуста")


def test_pizza_description(page: Page) -> None:

    with allure.step("Открыть главную страницу"):
        page.cart = PageCart(page)
        page.cart.open()
        logger.info("Главная страница открыта")

    with allure.step("Кликнуть по изображению пиццы"):
        page.cart.click_pizza_img()
        logger.info("Изображение пиццы выбрано")

    with allure.step("Проверить описание пиццы"):
        page.cart.checking_description_is_that_pizza()
        logger.info("Описание пиццы проверено")


def test_cart_change_count(page: Page) -> None:

    with allure.step("Открыть главную страницу"):
        page.cart = PageCart(page)
        page.cart.open()
        logger.info("Главная страница открыта")

    with allure.step("Добавить пиццу в корзину"):
        page.cart.add_pizza_to_cart()
        logger.info("Пицца добавлена в корзину")

    with allure.step("Перейти в корзину"):
        page.cart.in_to_cart()
        logger.info("Переход в корзину выполнен")

    with allure.step("Увеличить количество пицц на 1"):
        page.cart.increase_velue_in_cart()
        logger.info("Количество пицц увеличено")

    with allure.step("Обновить корзину"):
        page.cart.refresh_cart()
        logger.info("Корзина обновлена")

    with allure.step("Проверить, что количество пицц увеличилось"):
        page.cart.checking_cart_is_increase()
        logger.info("Количество пицц проверено")


def test_pizza_add_ingredient(page: Page) -> None:

    with allure.step("Открыть главную страницу"):
        page.cart = PageCart(page)
        page.cart.open()
        logger.info("Главная страница открыта")

    with allure.step("Кликнуть по изображению пиццы"):
        page.cart.click_pizza_img()
        logger.info("Изображение пиццы выбрано")

    with allure.step("Выбрать сырный борт для пиццы"):
        page.cart.choose_chees_bort_pizza()
        logger.info("Сырный борт выбран")

    with allure.step("Добавить пиццу с сырным бортом в корзину"):
        page.cart.add_pizza_with_chees_bort()
        logger.info("Пицца с сырным бортом добавлена в корзину")

    with allure.step("Перейти в корзину"):
        page.cart.in_to_cart()
        logger.info("Переход в корзину выполнен")

    with allure.step("Проверить, что пицца с сырным бортом в корзине"):
        expect(page.get_by_role("definition")).to_contain_text("Сырный борт")
        logger.info("Пицца с сырным бортом проверена")


def test_make_order(page: Page) -> None:

    with allure.step("Открыть главную страницу"):
        page.cart = PageCart(page)
        page.cart.open()
        logger.info("Главная страница открыта")

    with allure.step("Добавить пиццу в корзину"):
        page.cart.add_pizza_to_cart()
        logger.info("Пицца добавлена в корзину")

    with allure.step("Перейти в корзину"):
        page.cart.in_to_cart()
        logger.info("Переход в корзину выполнен")

    with allure.step("Перейти к оформлению заказа"):
        page.cart.menu_make_order()
        logger.info("Оформление заказа начато")

    with allure.step("Авторизоваться"):
        time.sleep(3)
        page.cart.clck_autorisation()
        page.cart.fill_imput_login()
        page.cart.fill_input_password()
        page.cart.clik_button_login()
        logger.info("Авторизация выполнена")

    with allure.step("Заполнить все поля для заказа"):
        page.cart.fill_all_feald()
        logger.info("Поля для заказа заполнены")

    with allure.step("Нажать кнопку 'Создать заказ'"):
        page.cart.click_make_order()
        logger.info("Заказ создан")

    with allure.step("Проверить, что заказ успешно создан"):
        page.cart.checking_maged_order()
        logger.info("Заказ проверен")


def test_apply_and_check_kupon(page: Page) -> None:

    with allure.step("Открыть главную страницу"):
        page.cart = PageCart(page)
        page.cart.open()
        logger.info("Главная страница открыта")

    with allure.step("Добавить пиццу в корзину"):
        page.cart.add_pizza_to_cart()
        logger.info("Пицца добавлена в корзину")

    with allure.step("Перейти в корзину"):
        page.cart.in_to_cart()
        logger.info("Переход в корзину выполнен")

    with allure.step("Ввести купон GIVEMEHALYAVA"):
        page.cart.fill_kupon_GIVEMEHALYAVA()
        logger.info("Купон введен")

    with allure.step("Применить купон"):
        page.cart.click_apply_kupon()
        logger.info("Купон применен")

    with allure.step("Проверить, что купон применен успешно"):
        page.cart.checking_kuppon_is_good()
        logger.info("Купон проверен")


def test_apply_kupon_twice_and_chek(page: Page) -> None:

    with allure.step("Открыть главную страницу"):
        page.cart = PageCart(page)
        page.cart.open()
        logger.info("Главная страница открыта")

    with allure.step("Перейти в меню 'Мой аккаунт'"):
        page.cart.menu_my_account()
        logger.info("Меню 'Мой аккаунт' открыто")

    with allure.step("Заполнить поле логина"):
        page.cart.fill_imput_login()
        logger.info("Поле логина заполнено")

    with allure.step("Заполнить поле пароля"):
        page.cart.fill_input_password()
        logger.info("Поле пароля заполнено")

    with allure.step("Нажать кнопку 'Войти'"):
        page.cart.clik_button_login()
        logger.info("Кнопка 'Войти' нажата")

    with allure.step("Проверить успешный вход"):
        page.cart.checking_have_to_login()
        logger.info("Вход выполнен успешно")
        page.cart.open()
    with allure.step("Добавить пиццу в корзину"):
        page.cart.add_pizza_to_cart()
        logger.info("Пицца добавлена в корзину")

    with allure.step("Перейти в корзину"):
        page.cart.in_to_cart()
        logger.info("Переход в корзину выполнен")

    with allure.step("Ввести купон GIVEMEHALYAVA"):
        page.cart.fill_kupon_GIVEMEHALYAVA()
        logger.info("Купон введен")

    with allure.step("Применить купон"):
        page.cart.click_apply_kupon()
        logger.info("Купон применен")

    with allure.step("Перейти к оформлению заказа"):
        page.cart.menu_make_order()
        logger.info("Оформление заказа начато")

    with allure.step("Заполнить все поля для заказа"):
        page.cart.fill_all_feald()
        logger.info("Поля для заказа заполнены")

    with allure.step("Нажать кнопку 'Создать заказ'"):
        page.cart.click_make_order()
        logger.info("Заказ создан")

    with allure.step("Проверить, что заказ успешно создан"):
        page.cart.checking_maged_order()
        logger.info("Заказ проверен")

    with allure.step("Проверить, что купон применен успешно"):
        page.cart.checking_kuppon_is_good()
        logger.info("Купон проверен")

    with allure.step("Обновить страницу"):
        page.reload()
    with allure.step("Открыть снаовуа главную страницу"):
        page.cart.open()
        logger.info("Страница открыта")

    with allure.step("Добавить пиццу в корзину"):
        page.cart.add_pizza_to_cart()
        logger.info("Пицца добавлена в корзину")

    with allure.step("Перейти в корзину"):
        page.cart.in_to_cart()
        logger.info("Переход в корзину выполнен")

    with allure.step("Ввести купон GIVEMEHALYAVA"):
        page.cart.fill_kupon_GIVEMEHALYAVA()
        logger.info("Купон введен")

    with allure.step("Применить купон"):
        page.cart.click_apply_kupon()
        logger.info("Купон применен")

    with allure.step("Проверить, что купон применен успешно"):
        page.cart.checking_kuppon_is_good()
        logger.info("Купон проверен")

    with allure.step("Перейти к оформлению заказа"):
        page.cart.menu_make_order()
        logger.info("Оформление заказа начато")

    with allure.step("Заполнить все поля для заказа"):
        page.cart.fill_all_feald()
        logger.info("Поля для заказа заполнены")

    with allure.step("Нажать кнопку 'Создать заказ'"):
        page.cart.click_make_order()
        logger.info("Заказ создан")

    with allure.step("Проверить, что заказ успешно создан"):
        page.cart.checking_maged_order()
        logger.info("Заказ проверен")


def test_fake_and_check_kupon(page: Page) -> None:

    with allure.step("Открыть главную страницу"):
        page.cart = PageCart(page)
        page.cart.open()
        logger.info("Главная страница открыта")

    with allure.step("Добавить пиццу в корзину"):
        page.cart.add_pizza_to_cart()
        logger.info("Пицца добавлена в корзину")

    with allure.step("Перейти в корзину"):
        page.cart.in_to_cart()
        logger.info("Переход в корзину выполнен")

    with allure.step("Ввести фейковый купон DC120"):
        page.cart.fill_facke_kupon_DC120()
        logger.info("Фейковый купон введен")

    with allure.step("Применить купон"):
        page.cart.click_apply_kupon()
        logger.info("Купон применен")

    with allure.step("Проверить, что купон недействителен"):
        page.cart.checking_fake_kuppon_is_no_good()
        logger.info("Фейковый купон проверен")


def test_block_request_kupon(page: Page) -> None:

    with allure.step("Открыть главную страницу"):
        page.cart = PageCart(page)
        page.cart.open()
        logger.info("Главная страница открыта")

    with allure.step("Добавить пиццу в корзину"):
        page.cart.add_pizza_to_cart()
        logger.info("Пицца добавлена в корзину")

    with allure.step("Перейти к оформлению заказа"):
        page.cart.menu_make_order()
        page.cart.menu_make_order()
        logger.info("Оформление заказа начато")

    with allure.step("Авторизоваться"):
        time.sleep(3)
        page.cart.autorisetion_get_order()
        logger.info("Авторизация выполнена")

    with allure.step("Отправить купон GIVEMEHALYAVA и заблокировать запрос"):
        page.cart.sent_kupon_GIVEMEHALYAVA__and_block_rquest()
        logger.info("Купон отправлен и запрос заблокирован")

    with allure.step("Заполнить данные и проверить"):
        page.cart.fill_data_and_check()
        logger.info("Данные заполнены и проверены")


def test_registration_bonus_program(page: Page) -> None:

    with allure.step("Открыть главную страницу"):
        page.cart = PageCart(page)
        page.cart.open()
        logger.info("Главная страница открыта")

    with allure.step("Заполнить данные для бонусной программы"):
        page.cart.fill_data_bonus()
        logger.info("Данные для бонусной программы заполнены")

    with allure.step("Нажать кнопку 'Получить бонус'"):
        page.cart.click_button_get_bonus()
        logger.info("Кнопка 'Получить бонус' нажата")

    with allure.step("Проверить регистрацию в бонусной программе"):
        page.cart.check_registration_bonus_program()
        logger.info("Регистрация в бонусной программе проверена")
