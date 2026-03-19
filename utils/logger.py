"""
Модуль логирования.
Настраивает запись логов в файл и в консоль.
"""
import logging
import os

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
LOG_FILE = os.path.join(LOG_DIR, "test_log.log")

os.makedirs(LOG_DIR, exist_ok=True)


def setup_logger(name: str = "test_logger") -> logging.Logger:
    """Создаёт и настраивает логгер."""
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(levelname)s - %(asctime)s - %(name)s - %(message)s"
    )

    # Запись в файл (все уровни)
    file_handler = logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Вывод в консоль (только INFO и выше)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    if not log.hasHandlers():
        log.addHandler(file_handler)
        log.addHandler(console_handler)

    return log


logger = setup_logger()
