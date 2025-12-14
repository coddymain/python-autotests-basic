UI Autotests (Python + Playwright)
README (RU)

Уровень проекта: Junior+ / Middle QA Automation

О проекте

Данный репозиторий содержит учебно-практический проект по UI-автоматизации тестирования веб-приложения (онлайн-пиццерия).

Проект ориентирован на уровень Junior+ / Middle QA Automation Engineer и демонстрирует умение:

строить архитектуру автотестов по Page Object Model;

писать читаемые и поддерживаемые UI-тесты;

работать с Playwright (sync API);

использовать pytest как основной тестовый фреймворк;

формировать Allure-отчёты;

подключать логирование и базовый code style.

Проект может использоваться как GitHub-портфолио при поиске работы.

Технологический стек

Python 3.10+

pytest

Playwright

pytest-playwright

Allure

flake8

logging

Структура проекта

pizzeria_tests/

├── tests/                  # UI-тесты

│   ├── test_cart.py         # Добавление товара в корзину

│   └── test_promo.py        # Применение промокода

├── pages/                  # Page Object слой

│   ├── base_page.py        # Базовый класс страницы

│   ├── home_page.py        # Главная страница

│   └── cart_page.py        # Корзина

├── utils/

│   └── logger.py           # Логирование

├── conftest.py             # pytest-фикстуры

├── requirements.txt        # Зависимости

├── pytest.ini              # Конфигурация pytest

├── .flake8                 # Code style

└── README.md               # Документация

Установка и запуск

Клонировать репозиторий

git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>

Создать виртуальное окружение

python -m venv venv
source venv/bin/activate      # macOS / Linux
venv\\Scripts\\activate         # Windows

Установить зависимости

pip install -r requirements.txt

Установить браузеры Playwright

playwright install
Запуск тестов
pytest

Запуск конкретного теста:

pytest tests/test_cart.py
Allure-отчёты

Генерация отчёта:

pytest --alluredir=reports

Просмотр:

allure serve reports
Реализованные проверки

добавление товара в корзину;

проверка, что корзина не пуста;

применение корректного промокода;

проверка изменения итоговой суммы.

Логирование

Ключевые действия логируются и выводятся:

в консоль;

в файл test_log.log.

CI / GitHub Actions

Проект подготовлен к подключению CI:

headless-запуск браузера;

запуск тестов по pytest;

генерация Allure-результатов.

Workflow может быть реализован с использованием GitHub Actions.

Ограничения

Зависимость от доступности тестового стенда.

Проверка скидки реализована в упрощённом виде и может быть расширена.

Идеи для развития

параметризация тестов;

явные ожидания;

негативные сценарии;

API-тесты;

полноценный CI с Allure.

README (EN)
About the project

This repository contains a UI test automation project for a demo web application (online pizzeria).

The project is designed for Junior+ / Middle QA Automation Engineers and demonstrates:

Page Object Model architecture;

UI automation using Playwright;

pytest as a test framework;

Allure reporting integration;

logging and basic code quality practices.

The project can be used as a GitHub portfolio example.

Tech stack

Python 3.10+

pytest

Playwright

pytest-playwright

Allure

flake8

logging

Run tests
pytest

Generate Allure report:

pytest --alluredir=reports
allure serve reports
CI / GitHub Actions

The project structure allows easy CI integration:

headless browser execution;

pytest-based test runs;

Allure results generation.

Author

Erastov Dmitriy

Автор: Ерастов Дмитрий
