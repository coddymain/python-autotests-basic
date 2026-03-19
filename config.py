"""
Конфигурация проекта.
Все настройки берутся из переменных окружения, а если их нет — используются значения по умолчанию.
"""
import os


class Config:
    BASE_URL = os.getenv("BASE_URL", "https://pizzeria.skillbox.cc")
    API_URL = os.getenv("API_URL", "https://pizzeria.skillbox.cc/wp-json/wp/v2")
    USER_LOGIN = os.getenv("USER_LOGIN", "erastov")
    USER_PASSWORD = os.getenv("USER_PASSWORD", "12345")
