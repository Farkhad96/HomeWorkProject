from collections import Counter

import pytest

from src.processing import filter_by_state, process_bank_operations, process_bank_search, sort_by_date


@pytest.fixture
def sample_transactions():
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2024-11-10T12:00:00",
            "description": "Оплата услуг связи",
        },
        {
            "id": 2,
            "state": "CANCELED",
            "date": "2023-01-01T09:00:00",
            "description": "Перевод клиенту",
        },
        {
            "id": 3,
            "state": "EXECUTED",
            "date": "2024-01-15T08:30:00",
            "description": "Оплата налогов",
        },
        {
            "id": 4,
            "state": "PENDING",
            "date": "2022-05-20T20:10:00",
            "description": "Перевод между своими счетами",
        },
        {
            "id": 5,
            "state": "EXECUTED",
            "date": "2024-12-31T23:59:59",
            "description": "Покупка продуктов",
        },
    ]


# ---------- filter_by_state ----------


def test_filter_by_state_default(sample_transactions):
    result = filter_by_state(sample_transactions)  # по умолчанию EXECUTED
    assert len(result) == 3
    assert all(item["state"] == "EXECUTED" for item in result)


def test_filter_by_state_specific(sample_transactions):
    result = filter_by_state(sample_transactions, "CANCELED")
    assert len(result) == 1
    assert all(item["state"] == "CANCELED" for item in result)


def test_filter_by_state_not_found(sample_transactions):
    result = filter_by_state(sample_transactions, "UNKNOWN")
    assert result == []


# ---------- sort_by_date ----------


def test_sort_by_date_descending(sample_transactions):
    result = sort_by_date(sample_transactions, descending=True)
    dates = [item["date"] for item in result]
    # проверяем, что даты отсортированы по убыванию
    assert dates == sorted(dates, reverse=True)


def test_sort_by_date_ascending(sample_transactions):
    result = sort_by_date(sample_transactions, descending=False)
    dates = [item["date"] for item in result]
    # проверяем, что даты отсортированы по возрастанию
    assert dates == sorted(dates)


def test_sort_by_date_empty_list():
    result = sort_by_date([])
    assert result == []


# ---------- process_bank_search ----------


def test_process_bank_search_found(sample_transactions):
    result = process_bank_search(sample_transactions, "оплата")
    # должны найти "Оплата услуг связи" и "Оплата налогов"
    descriptions = [item["description"].lower() for item in result]
    assert len(result) == 2
    assert "оплата услуг связи" in descriptions
    assert "оплата налогов" in descriptions


def test_process_bank_search_case_insensitive(sample_transactions):
    result = process_bank_search(sample_transactions, "ПЕРЕВОД")
    descriptions = [item["description"].lower() for item in result]
    assert len(result) == 2
    assert "перевод клиенту" in descriptions
    assert "перевод между своими счетами" in descriptions


def test_process_bank_search_not_found(sample_transactions):
    result = process_bank_search(sample_transactions, "несуществующая строка")
    assert result == []


# ---------- process_bank_operations ----------


def test_process_bank_operations_basic(sample_transactions):
    categories = [
        "Оплата услуг связи",
        "Оплата налогов",
        "Покупка продуктов",
    ]
    result = process_bank_operations(sample_transactions, categories)

    # ожидаем Counter с количеством по категориям
    assert isinstance(result, Counter)
    assert result["Оплата услуг связи"] == 1
    assert result["Оплата налогов"] == 1
    assert result["Покупка продуктов"] == 1
    # категорий, которых нет в данных, быть не должно
    assert "Перевод клиенту" not in result


def test_process_bank_operations_no_categories_match(sample_transactions):
    categories = ["Аренда жилья", "Путешествия"]
    result = process_bank_operations(sample_transactions, categories)
    assert isinstance(result, Counter)
    assert result == Counter()


def test_process_bank_operations_empty_transactions():
    result = process_bank_operations([], ["Категория"])
    assert isinstance(result, Counter)
    assert result == Counter()
