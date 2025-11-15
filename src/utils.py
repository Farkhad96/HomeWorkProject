import json
import logging
from typing import Any, Dict, List

logger = logging.getLogger("utils")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("../logs/utils.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s : %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает список финансовых транзакций из JSON-файла.

    Условия:
    - Если файл не найден → вернуть пустой список.
    - Если файл пустой → вернуть пустой список.
    - Если в корне JSON не список → вернуть пустой список.

    Параметры:
        file_path: Путь до JSON-файла (например, "..data/operations.json").

    Возвращает:
        Список словарей (транзакций). Если что-то не так — [].
    """
    logger.info(f"Функция load_transactions приняла на вход {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            logger.info(f"Загружен файл мз {file_path} ")
            if not data:
                logger.info("Файл пустой, возвращается пустой список")
                return []
            if isinstance(data, list):
                logger.info("Файл прочитан успешно")
                return data
            return []
    except (FileNotFoundError, json.JSONDecodeError) as ex:
        logger.info(f"Произошла ошибка {ex}")
        return []
