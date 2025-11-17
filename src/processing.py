import re
from collections import Counter
from typing import Any, Dict, List


def filter_by_state(transaction_data: List[Dict], state: str = "EXECUTED") -> List[Dict]:
    """
    Функция фильтрует список словарей по значению ключа 'state'.

    transaction_data: Список словарей для фильтрации.
    state: Значение для ключа 'state' (по умолчанию 'EXECUTED').
    """
    return [item for item in transaction_data if item.get("state") == state.upper()]


def sort_by_date(transaction_data: List[Dict], descending: bool = True) -> List[Dict]:
    """
    Функция сортирует список словарей по дате.

    transaction_data: Список словарей для сортировки. Каждый словарь должен содержать ключ 'date'.
    descending: Параметр, определяющий порядок сортировки (по умолчанию True — убывание).
    """

    # Сортировка списка словарей по дате
    return sorted(transaction_data, key=lambda x: x["date"], reverse=descending)


def process_bank_search(transaction_data: list[dict], search: Any) -> list[dict]:
    """
    функция принимает список словарей с данными о банковских операциях и строку поиска
    и возвращает список словарей, у которых в описании есть данная строка.

    transaction_data: Список словарей для поиска
    search: Строка для поиска
    """

    return [item for item in transaction_data if re.search(search, item.get("description"), flags=re.IGNORECASE)]


def process_bank_operations(transaction_data: list[dict], categories: list) -> dict:
    """
    функция принимает список словарей с данными о банковских операциях
    и список категорий операций, а возвращает словарь, в котором ключи — это названия категорий,
    а значения — это количество операций в каждой категории.

    :param transaction_data: Список словарей с данными о банковских операциях
    :param categories: список категорий операций
    :return: словарь, в котором ключи — это названия категорий,
    а значения — это количество операций в каждой категории.
    """

    descriptions = [item.get("description") for item in transaction_data if item.get("description") in categories]
    counted = Counter(descriptions)
    return counted
