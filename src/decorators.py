# decorators.py
import logging
import functools
import time


def setup_logging(filename=None):
    """Настройка логирования."""
    if filename:
        logging.basicConfig(filename=filename, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
    else:
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')


def log(filename=None):
    """Декоратор для логирования информации о функции."""
    setup_logging(filename)  # Настраиваем логирование

    def decorator(func):
        @functools.wraps(func)  # Сохраняем метаданные функции
        def wrapper(*args, **kwargs):
            logging.info(f"Начало выполнения функции '{func.__name__}' с аргументами: args={args}, kwargs={kwargs}")
            start_time = time.time()

            try:
                # Выполняем функцию и сохраняем результат
                result = func(*args, **kwargs)
                logging.info(f"Функция '{func.__name__}' завершена успешно. Результат: {result}")
                return result
            except Exception as e:
                # Логируем информацию об ошибке
                logging.error(
                    f"Ошибка в функции '{func.__name__}': {type(e).__name__} - {e}. Аргументы: args={args}, kwargs={kwargs}")
                raise  # Перебрасываем исключение дальше
            finally:
                # Логируем время выполнения функции
                end_time = time.time()
                execution_time = end_time - start_time
                logging.info(f"Время выполнения функции '{func.__name__}': {execution_time:.4f} секунд")

        return wrapper

    return decorator