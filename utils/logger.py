
import logging
import sys
import os

# Добавляем корневую папку проекта в PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Настройки логирования
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "test_log.log")

# Создаем папку для логов, если её нет
os.makedirs(LOG_DIR, exist_ok=True)

def setup_logger(name="test_logger"):
    """Настройка логирования в файл и консоль."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Логируем всё

    # Формат логов
    log_format = logging.Formatter("%(levelname)s - %(asctime)s - %(name)s - %(message)s")

    # Обработчик для файла (DEBUG и выше)
    file_handler = logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(log_format)

    # Обработчик для консоли (INFO и выше)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(log_format)

    # Добавляем обработчики в логгер
    if not logger.hasHandlers():
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

# Глобальный логгер
logger = setup_logger()


