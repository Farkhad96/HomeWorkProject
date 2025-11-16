import json
import logging
from typing import Any, Dict, List

import pandas as pd

logger = logging.getLogger("utils")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("../logs/utils.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s : %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def _row_to_transaction(row: pd.Series) -> Dict[str, Any]:
    """
    Преобразует строку DataFrame в транзакцию того же формата,
    который использовался в JSON (с полем operationAmount).
    Ожидаются колонки:
    id, state, date, amount, currency_name, currency_code, from, to, description
    """

    def _clean(value: Any) -> Any:
        # В pandas пропуски часто NaN → превращаем в None
        return None if pd.isna(value) else value

    return {
        "id": str(row["id"]),
        "state": str(row["state"]),
        "date": str(row["date"]),
        "operationAmount": {
            "amount": str(row["amount"]),
            "currency": {
                "name": str(row["currency_name"]),
                "code": str(row["currency_code"]),
            },
        },
        "from": _clean(row["from"]),
        "to": _clean(row["to"]),
        "description": str(row["description"]),
    }


def load_transactions_json(file_path: str) -> List[Dict[str, Any]]:
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


def load_transactions_csv(file_path: str) -> List[Dict[str, Any]]:
    """
    Считывает финансовые операции из CSV-файла и возвращает список транзакций
    в том же формате, что и JSON (см. _row_to_transaction).

    Для файла transactions.csv используется разделитель ';'.
    """
    logger.info(f"Функция load_transactions_csv приняла на вход {file_path}")
    try:
        df = pd.read_csv(file_path, sep=";")
    except FileNotFoundError as ex:
        logger.info(f"Файл не найден: {ex}")
        return []
    except pd.errors.EmptyDataError as ex:
        logger.info(f"Файл пустой или некорректный: {ex}")
        return []

    if df.empty:
        logger.info("CSV-файл пустой, возвращается пустой список")
        return []

    transactions: List[Dict[str, Any]] = []
    for _, row in df.iterrows():
        transactions.append(_row_to_transaction(row))

    logger.info(f"CSV-файл {file_path} успешно прочитан, загружено {len(transactions)} операций")
    return transactions


def load_transactions_excel(file_path: str) -> List[Dict[str, Any]]:
    """
    Считывает финансовые операции из XLSX-файла и возвращает список транзакций
    в том же формате, что и JSON (см. _row_to_transaction).
    """
    logger.info(f"Функция load_transactions_excel приняла на вход {file_path}")
    try:
        df = pd.read_excel(file_path)
    except FileNotFoundError as ex:
        logger.info(f"Файл не найден: {ex}")
        return []
    except ValueError as ex:
        # на случай проблем с форматом файла
        logger.info(f"Ошибка чтения Excel-файла: {ex}")
        return []

    if df.empty:
        logger.info("Excel-файл пустой, возвращается пустой список")
        return []

    transactions: List[Dict[str, Any]] = []
    for _, row in df.iterrows():
        transactions.append(_row_to_transaction(row))

    logger.info(f"Excel-файл {file_path} успешно прочитан, загружено {len(transactions)} операций")
    return transactions


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Универсальная функция:
    - *.json  → load_transactions_json
    - *.csv   → load_transactions_csv
    - *.xlsx  → load_transactions_excel

    Если расширение неизвестно — возвращает [].
    """
    logger.info(f"Функция load_transactions приняла на вход {file_path}")

    lower = file_path.lower()
    if lower.endswith(".json"):
        return load_transactions_json(file_path)
    if lower.endswith(".csv"):
        return load_transactions_csv(file_path)
    if lower.endswith(".xlsx"):
        return load_transactions_excel(file_path)

    logger.info("Неизвестное расширение файла, возвращается пустой список")
    return []
