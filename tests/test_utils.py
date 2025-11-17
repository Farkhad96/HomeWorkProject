# tests/test_utils_new.py
import json

import pandas as pd
import pytest

from src import utils

# --- find_project_root ------------------------------------------------------


def test_find_project_root_finds_pyproject(tmp_path, monkeypatch):
    """
    Строим фальшивую структуру:
    tmp/
        pyproject.toml
        a/
          b/
             test_file.py

    И проверяем, что find_project_root, запущенный из a/b, вернет tmp.
    """
    # создаем корень проекта
    project_root = tmp_path
    (project_root / "pyproject.toml").write_text("[tool.fake]\n", encoding="utf-8")

    # вложенные директории
    nested_dir = project_root / "a" / "b"
    nested_dir.mkdir(parents=True)

    start_file = nested_dir / "test_file.py"
    start_file.write_text("# dummy", encoding="utf-8")

    root = utils.find_project_root(start=start_file)
    assert root == project_root


def test_find_project_root_raises_if_no_pyproject(tmp_path):
    """
    Если pyproject.toml нигде нет, должно бросаться RuntimeError.
    """
    some_dir = tmp_path / "some"
    some_dir.mkdir()
    start_file = some_dir / "test.py"
    start_file.write_text("# dummy", encoding="utf-8")

    with pytest.raises(RuntimeError):
        utils.find_project_root(start=start_file)


# --- load_transactions_json -------------------------------------------------


def test_load_transactions_json_ok(tmp_path):
    """
    Корректный JSON-файл со списком операций.
    """
    data = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "CANCELED"},
    ]
    file_path = tmp_path / "operations.json"
    file_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    result = utils.load_transactions_json(str(file_path))
    assert result == data
    assert isinstance(result, list)
    assert len(result) == 2


def test_load_transactions_json_empty_file(tmp_path):
    """
    Пустой JSON (файл содержит [], или вообще пустой) -> [].
    """
    file_path = tmp_path / "empty.json"
    file_path.write_text("[]", encoding="utf-8")

    result = utils.load_transactions_json(str(file_path))
    assert result == []


def test_load_transactions_json_not_a_list(tmp_path):
    """
    В корне JSON не список -> [].
    """
    file_path = tmp_path / "dict.json"
    file_path.write_text(json.dumps({"a": 1}), encoding="utf-8")

    result = utils.load_transactions_json(str(file_path))
    assert result == []


def test_load_transactions_json_file_not_found(tmp_path):
    """
    Файла нет -> [].
    """
    file_path = tmp_path / "no_such_file.json"
    result = utils.load_transactions_json(str(file_path))
    assert result == []


def test_load_transactions_json_broken_json(tmp_path):
    """
    Некорректный JSON -> [].
    """
    file_path = tmp_path / "broken.json"
    file_path.write_text("{not json", encoding="utf-8")

    result = utils.load_transactions_json(str(file_path))
    assert result == []


# --- load_transactions_csv --------------------------------------------------


def test_load_transactions_csv_ok(tmp_path):
    """
    CSV со строками, которые преобразуются в транзакции через _row_to_transaction.
    Проверяем несколько ключевых полей.
    """
    file_path = tmp_path / "transactions.csv"

    # создаем DataFrame в том формате, который ожидает _row_to_transaction
    df = pd.DataFrame(
        [
            {
                "id": 1,
                "state": "EXECUTED",
                "date": "2024-01-01T10:00:00",
                "amount": 100.5,
                "currency_name": "Рубль",
                "currency_code": "RUB",
                "from": "1234567890123456",
                "to": "40817810000000000001",
                "description": "Оплата услуг",
            },
            {
                "id": 2,
                "state": "CANCELED",
                "date": "2024-01-02T12:00:00",
                "amount": 200,
                "currency_name": "Доллар",
                "currency_code": "USD",
                "from": None,
                "to": "40817810000000000002",
                "description": "Покупка",
            },
        ]
    )

    df.to_csv(file_path, sep=";", index=False)

    result = utils.load_transactions_csv(str(file_path))
    assert isinstance(result, list)
    assert len(result) == 2

    first = result[0]
    assert first["id"] == "1"
    assert first["state"] == "EXECUTED"
    assert first["operationAmount"]["amount"] == "100.5"
    assert first["operationAmount"]["currency"]["code"] == "RUB"
    assert first["from"] == "1234567890123456"
    assert first["description"] == "Оплата услуг"


def test_load_transactions_csv_file_not_found(tmp_path):
    file_path = tmp_path / "no_such.csv"
    result = utils.load_transactions_csv(str(file_path))
    assert result == []


def test_load_transactions_csv_empty_file(tmp_path):
    """
    Пустой CSV -> [] (через EmptyDataError или пустой df).
    """
    file_path = tmp_path / "empty.csv"
    # создаем реально пустой файл
    file_path.write_text("", encoding="utf-8")

    result = utils.load_transactions_csv(str(file_path))
    assert result == []


# --- load_transactions_excel -----------------------------------------------


def test_load_transactions_excel_ok(tmp_path):
    """
    Excel-файл в формате, подходящем под _row_to_transaction.
    """
    file_path = tmp_path / "transactions.xlsx"

    df = pd.DataFrame(
        [
            {
                "id": 10,
                "state": "EXECUTED",
                "date": "2024-02-01T09:00:00",
                "amount": 500,
                "currency_name": "Рубль",
                "currency_code": "RUB",
                "from": "1111222233334444",
                "to": "40817810000000000010",
                "description": "Перевод",
            }
        ]
    )
    df.to_excel(file_path, index=False)

    result = utils.load_transactions_excel(str(file_path))
    assert isinstance(result, list)
    assert len(result) == 1

    trx = result[0]
    assert trx["id"] == "10"
    assert trx["state"] == "EXECUTED"
    assert trx["operationAmount"]["amount"] == "500"
    assert trx["operationAmount"]["currency"]["code"] == "RUB"
    assert trx["description"] == "Перевод"


def test_load_transactions_excel_file_not_found(tmp_path):
    file_path = tmp_path / "no_such.xlsx"
    result = utils.load_transactions_excel(str(file_path))
    assert result == []


def test_load_transactions_excel_empty_file(tmp_path):
    """
    Пустой Excel — в твоей реализации будет либо ValueError, либо пустой df.
    Проверим, что функция вернёт [].
    """
    file_path = tmp_path / "empty.xlsx"

    # создаём валидный Excel с пустым DataFrame
    df = pd.DataFrame(
        columns=["id", "state", "date", "amount", "currency_name", "currency_code", "from", "to", "description"]
    )
    df.to_excel(file_path, index=False)

    result = utils.load_transactions_excel(str(file_path))
    assert result == []


# --- load_transactions (универсальная обёртка) -----------------------------


def test_load_transactions_dispatch_json(tmp_path, monkeypatch):
    file_path = tmp_path / "operations.json"
    file_path.write_text("[]", encoding="utf-8")

    called = {}

    def fake_json_loader(path):
        called["json"] = path
        return [{"id": 1}]

    monkeypatch.setattr(utils, "load_transactions_json", fake_json_loader)

    result = utils.load_transactions(str(file_path))
    assert called["json"] == str(file_path)
    assert result == [{"id": 1}]


def test_load_transactions_dispatch_csv(tmp_path, monkeypatch):
    file_path = tmp_path / "transactions.csv"
    file_path.write_text("", encoding="utf-8")

    called = {}

    def fake_csv_loader(path):
        called["csv"] = path
        return [{"id": 2}]

    monkeypatch.setattr(utils, "load_transactions_csv", fake_csv_loader)

    result = utils.load_transactions(str(file_path))
    assert called["csv"] == str(file_path)
    assert result == [{"id": 2}]


def test_load_transactions_dispatch_excel(tmp_path, monkeypatch):
    file_path = tmp_path / "transactions.xlsx"
    file_path.write_text("", encoding="utf-8")

    called = {}

    def fake_excel_loader(path):
        called["xlsx"] = path
        return [{"id": 3}]

    monkeypatch.setattr(utils, "load_transactions_excel", fake_excel_loader)

    result = utils.load_transactions(str(file_path))
    assert called["xlsx"] == str(file_path)
    assert result == [{"id": 3}]


def test_load_transactions_unknown_extension(tmp_path):
    """
    Неизвестное расширение -> [].
    """
    file_path = tmp_path / "transactions.txt"
    file_path.write_text("whatever", encoding="utf-8")

    result = utils.load_transactions(str(file_path))
    assert result == []
