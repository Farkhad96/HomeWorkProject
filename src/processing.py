from typing import List, Dict


def filter_by_state(transaction_data: List[Dict], state: str = "EXECUTED") -> List[Dict]:
    """
    Функция фильтрует список словарей по значению ключа 'state'.

    data: Список словарей для фильтрации.
    state: Значение для ключа 'state' (по умолчанию 'EXECUTED').
    """
    return [item for item in transaction_data if item.get("state") == state]


def sort_by_date(transaction_data: List[Dict], descending: bool = True) -> List[Dict]:
    """
    Функция сортирует список словарей по дате.

    data: Список словарей для сортировки. Каждый словарь должен содержать ключ 'date'.
    descending: Параметр, определяющий порядок сортировки (по умолчанию True — убывание).
    """

    # Сортировка списка словарей по дате
    return sorted(transaction_data, key=lambda x: x["date"], reverse=descending)
