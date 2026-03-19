# Python Autotests Basic (Middle-level Refactored)

Этот проект представляет собой автоматизированный набор тестов для учебного стенда "Пиццерия" (Skillbox). Проект доведен до стандарта **Middle-level QA Automation**.

## Основные изменения (Refactoring)

- **Page Object Model (POM)**: Полное разделение локаторов и логики. Локаторы вынесены во вложенный класс `Locators`.
- **BasePage**: Создан базовый класс с общими методами (click, fill, wait) и типизацией.
- **Fixtures**: Использование фикстур `pytest` для управления жизненным циклом страниц и данных (см. `conftest.py`).
- **API Helper**: Написан удобный хелпер для работы с API, который автоматически логирует запросы и добавляет шаги в Allure.
- **Data Management**: Тестовые данные (купоны, данные пользователей) вынесены в `data/test_data.py`.
- **Logging**: Настроено детальное логирование всех действий.
- **Reporting**: Интеграция с Allure (шаги, заголовки, скриншоты при провалах).
- **CI/CD**: Настроен GitHub Actions для автоматического запуска тестов.

## Структура проекта

- `pages/`: Объекты страниц (Page Objects).
- `tests/ui/`: UI-тесты (Playwright).
- `tests/api/`: API-тесты (Requests/APIHelper).
- `data/`: Тестовые данные и константы.
- `utils/`: Утилиты (логгер, API-хелпер).
- `config.py`: Конфигурация проекта (URL, логины).
- `conftest.py`: Фикстуры pytest.
- `.github/workflows/`: Настройки CI/CD.

## Как запустить

1.  **Создать виртуальное окружение**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
2.  **Установить зависимости**:
    ```bash
    pip install -r requirements.txt
    playwright install
    ```
3.  **Запустить тесты**:
    ```bash
    pytest --alluredir=allure-results
    ```
4.  **Посмотреть отчет**:
    ```bash
    allure serve allure-results
    ```

## Конфигурация
Все настройки находятся в `config.py`. Вы можете переопределить их через переменные окружения:
- `BASE_URL`: URL сайта
- `HEADLESS`: `true`/`false` (по умолчанию `true`)
