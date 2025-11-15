import json
from typing import Any, Dict, List


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
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not data:
                return []
            if isinstance(data, list):
                return data
            return []
    except (FileNotFoundError, json.JSONDecodeError):
        return []
