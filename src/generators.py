from typing import Generator


def filter_by_currency(list_of_transactions : list[dict], name_of_currency : str )-> Generator[dict]:
    """Функция принимает на вход список словарей, представляющих
    транзакции и возвращает итератор, который поочередно выдает
    транзакции, где валюта операции соответствует заданной"""

    filtered_transactions = filter(lambda x: x.get("operationAmount",{}).get("currency",{}).get("name",{}) == name_of_currency, list_of_transactions)
    for transaction in filtered_transactions:
        yield transaction
def transaction_descriptions (list_of_transactions : list[dict]) -> Generator[str]:
    """генератор, который принимает список словарей с транзакциями и возвращает описание каждой операции по очереди."""

    for transaction in list_of_transactions:
        yield transaction.get("description","")
def card_number_generator (first_number : int, last_number : int)-> Generator[str]:
    """генератор, который выдает номера банковских карт в формате XXXX XXXX XXXX XXXX, где X — цифра номера карты. Генератор может сгенерировать номера карт в заданном диапазоне от 0000 0000 0000 0001 до 9999 9999 9999 9999."""

    for number in range(first_number, last_number+1):
        number_string = f"{number:016d}"
        chunks = [number_string[i: i + 4] for i in range(0, 16, 4)]
        resulting_number_string: str = " ".join(chunks)
        yield resulting_number_string
