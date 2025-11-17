from datetime import datetime

import src.masks

list_of_card_names: list = [
    "Счет",
    "Maestro",
    "MasterCard",
    "Visa Classic",
    "Visa Platinum",
    "Visa Gold",
    "Troy",
    "МИР",
    "American Express",
    "Discover",
]


def is_iso_datetime(s: str) -> bool:
    """Функция проверяет дату га соответствие формату ISO"""
    try:
        datetime.fromisoformat(s)
        return True
    except ValueError:
        return False


def mask_account_card(card_account_number: str) -> str:
    """Функция принимает номер карты или номер счета, возвращает маскированный номер"""
    card_number = ""
    for i in range(len(card_account_number)):
        if card_account_number[-i - 1].isdigit():
            card_number = card_account_number[-i - 1] + card_number
        else:
            break
    if card_account_number[: -1 - len(card_number)] not in list_of_card_names:
        return "Данные некорректные"
    if card_account_number[: -1 - len(card_number)] == "Счет":
        result_account_number = src.masks.get_mask_account(card_number)
        if result_account_number == "Неправильно набран номер":
            return "Данные некорректные"
        return "Счет " + result_account_number
    else:
        result_card_number = src.masks.get_mask_card_number(card_number)
        if result_card_number == "Неправильно набран номер":
            return "Данные некорректные"
        return card_account_number[: -len(card_number)] + result_card_number


def get_date(date_str: str) -> str:
    """Функция принимает дату в формате ISO, возвращает дату в формате дд.мм.гг"""
    if is_iso_datetime(date_str):
        dt = datetime.fromisoformat(date_str)
        return dt.strftime("%d.%m.%Y")
    else:
        return "Данные некорректные"
