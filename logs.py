import logging
import os
from logging.handlers import TimedRotatingFileHandler
import sys
from config import settings

def setup_logging():
    log_levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
    }
    log_level = log_levels[settings.LOG_LEVEL.upper()]

    os.makedirs("logs", exist_ok=True)

    # Формат логов
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s"
    formatter = logging.Formatter(log_format)

    # --- Файловый обработчик (ротация каждый день) ---
    file_handler = TimedRotatingFileHandler(
        filename='./logs/app.log',
        when='midnight',
        interval=1,
        backupCount=10,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)

    # --- Консольный обработчик ---
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)  # В консоль можно выводить больше информации

    # --- Настройка корневого логгера ---
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)  # Минимальный уровень для файла
    root_logger.handlers.clear()  # Очищаем все старые обработчики
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    # --- Настройка логгеров Uvicorn/FastAPI ---
    uvicorn_loggers = ("uvicorn", "uvicorn.error", "uvicorn.access", "fastapi")
    for logger_name in uvicorn_loggers:
        logger = logging.getLogger(logger_name)
        logger.handlers.clear()
        logger.propagate = True  # Передаем логи в корневой логгер
        logger.setLevel(log_level)  # Уровень для самого логгера

