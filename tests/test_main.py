import types

import pytest

import main


@pytest.fixture
def fake_modules(monkeypatch):
    """
    Подменяем модули src.utils, src.processing, src.generators, src.widget
    на простые заглушки, чтобы управлять данными в тестах.
    """

    # ---- src.utils ----
    fake_utils = types.SimpleNamespace()

    def fake_load_transactions(path):
        # Разные файлы будем различать по пути для тестов
        if path.endswith("operations.json"):
            # Набор 1 — для JSON
            return [
                {
                    "id": 1,
                    "state": "EXECUTED",
                    "date": "2024-01-02T10:00:00",
                    "description": "Оплата услуг связи",
                    "from": "Счет 43475624104328495820",
                    "to": "Счет 43475624104328495820",
                    "operationAmount": {
                        "amount": "100.50",
                        "currency": {"code": "RUB"},
                    },
                },
                {
                    "id": 2,
                    "state": "EXECUTED",
                    "date": "2024-01-01T09:00:00",
                    "description": "Покупка продуктов",
                    "from": None,
                    "to": "Счет 43475624104328495820",
                    "operationAmount": {
                        "amount": "200",
                        "currency": {"code": "USD"},
                    },
                },
                {
                    "id": 3,
                    "state": "CANCELED",
                    "date": "2024-01-03T09:00:00",
                    "description": "Перевод клиенту",
                    "from": "Счет 43475624104328495820",
                    "to": "Счет 43475624104328495820",
                    "operationAmount": {
                        "amount": "300",
                        "currency": {"code": "RUB"},
                    },
                },
            ]
        elif path.endswith("transactions.csv"):
            # Набор 2 — для CSV
            return [
                {
                    "id": 10,
                    "state": "EXECUTED",
                    "date": "2023-12-31T23:59:59",
                    "description": "Оплата налогов",
                    "from": None,
                    "to": "Счет 43475624104328495820",
                    "operationAmount": {
                        "amount": "500",
                        "currency": {"code": "RUB"},
                    },
                }
            ]
        elif path.endswith("transactions_excel.xlsx"):
            # Набор 3 — для XLSX — пустой список, чтобы отработала ветка "ничего не найдено"
            return []
        else:
            return []

    fake_utils.load_transactions = fake_load_transactions

    # ---- src.processing ----
    fake_processing = types.SimpleNamespace()

    def fake_filter_by_state(transactions, state):
        return [t for t in transactions if t.get("state") == state.upper()]

    def fake_sort_by_date(transactions, descending=True):
        return sorted(transactions, key=lambda x: x["date"], reverse=descending)

    def fake_process_bank_search(transactions, search):
        import re

        return [
            t
            for t in transactions
            if t.get("description") and re.search(search, t["description"], flags=re.IGNORECASE)
        ]

    fake_processing.filter_by_state = fake_filter_by_state
    fake_processing.sort_by_date = fake_sort_by_date
    fake_processing.process_bank_search = fake_process_bank_search

    # ---- src.generators ----
    fake_generators = types.SimpleNamespace()

    def fake_filter_by_currency(transactions, code):
        for transaction in transactions:
            if transaction.get("operationAmount", {}).get("currency", {}).get("code") == code:
                yield transaction

    fake_generators.filter_by_currency = fake_filter_by_currency

    # ---- src.widget ----
    fake_widget = types.SimpleNamespace()

    def fake_get_date(date_str):
        return date_str[:10] if date_str else ""

    def fake_mask_account_card(number):
        if not number:
            return ""
        return "****" + str(number)[-4:]

    fake_widget.get_date = fake_get_date
    fake_widget.mask_account_card = fake_mask_account_card

    # Подменяем в модуле main атрибут src
    monkeypatch.setattr(
        main,
        "src",
        types.SimpleNamespace(
            utils=fake_utils,
            processing=fake_processing,
            generators=fake_generators,
            widget=fake_widget,
        ),
    )


# --------------------------------------------------------------------
# Тесты основных сценариев
# --------------------------------------------------------------------


def test_json_rub_with_search_sort_asc(monkeypatch, capsys, fake_modules):
    """
    Сценарий:
    - меню: JSON (1)
    - статус: executed
    - сортировать: да
    - по возрастанию
    - только RUB: да
    - фильтрация по описанию: да, по слову "оплата"
    Ожидаем одну RUB-транзакцию с "Оплата услуг связи".
    """
    user_inputs = iter(
        [
            "1",  # пункт меню -> JSON
            "executed",  # статус
            "да",  # сортировать по дате?
            "по возрастанию",  # порядок сортировки
            "да",  # только рублевые?
            "да",  # фильтрация по слову в описании?
            "оплата",  # слово для поиска
        ]
    )
    monkeypatch.setattr(
        "builtins.input",
        lambda *args, **kwargs: next(user_inputs),
    )

    main.main()
    captured = capsys.readouterr()
    out = captured.out

    # Общие строки
    assert "Привет! Добро пожаловать в программу работы с банковскими транзакциями." in out
    assert "Для обработки выбран JSON-файл." in out
    assert "Операции отфильтрованы по статусу executed" in out
    assert "Распечатываю итоговый список транзакций..." in out
    assert "Всего банковских операций в выборке: 1" in out
    assert "Оплата услуг связи" in out

    # USD-транзакция и CANCELED не должны попасть в итоговую выборку
    assert "Покупка продуктов" not in out
    assert "Перевод клиенту" not in out


def test_json_no_sort_no_rub_no_description_filter(monkeypatch, capsys, fake_modules):
    """
    Сценарий:
    - меню: JSON (1)
    - статус: EXECUTED
    - сортировать: нет
    - только RUB: нет (оставляем EXECUTED, RUB+USD)
    - фильтрация по описанию: нет
    Ожидаем 2 операции (EXECUTED: RUB+USD).
    """
    user_inputs = iter(
        [
            "1",  # пункт меню -> JSON
            "EXECUTED",  # статус
            "нет",  # сортировать по дате?
            "нет",  # только рублевые?
            "нет",  # фильтрация по слову в описании?
        ]
    )
    monkeypatch.setattr(
        "builtins.input",
        lambda *args, **kwargs: next(user_inputs),
    )

    main.main()
    captured = capsys.readouterr()
    out = captured.out

    assert "Для обработки выбран JSON-файл." in out
    assert "Операции отфильтрованы по статусу EXECUTED" in out
    assert "Распечатываю итоговый список транзакций..." in out
    assert "Всего банковских операций в выборке: 2" in out

    # Обе EXECUTED должны быть
    assert "Оплата услуг связи" in out
    assert "Покупка продуктов" in out

    # CANCELED не должен быть
    assert "Перевод клиенту" not in out


def test_csv_sort_desc_and_rub_only_without_search(monkeypatch, capsys, fake_modules):
    """
    Сценарий для CSV:
    - меню: CSV (2)
    - статус: EXECUTED
    - сортировать: да
    - по убыванию
    - только RUB: да
    - фильтрация по описанию: нет
    Должна быть одна операция "Оплата налогов".
    """
    user_inputs = iter(
        [
            "2",  # пункт меню -> CSV
            "EXECUTED",  # статус
            "да",  # сортировать по дате?
            "по убыванию",  # порядок
            "да",  # только рублевые
            "нет",  # без фильтра по описанию
        ]
    )
    monkeypatch.setattr(
        "builtins.input",
        lambda *args, **kwargs: next(user_inputs),
    )

    main.main()
    captured = capsys.readouterr()
    out = captured.out

    assert "Для обработки выбран CSV-файл." in out
    assert "Операции отфильтрованы по статусу EXECUTED" in out
    assert "Распечатываю итоговый список транзакций..." in out
    assert "Всего банковских операций в выборке: 1" in out
    assert "Оплата налогов" in out


def test_xlsx_no_transactions(monkeypatch, capsys, fake_modules):
    """
    Сценарий для XLSX:
    - меню: XLSX (3)
    - статус: EXECUTED

    Так как в fake_load_transactions для XLSX возвращается [],
    фильтрация по статусу даст пустой список, должна отработать ветка "операций не найдено".
    """
    user_inputs = iter(
        [
            "3",  # пункт меню -> XLSX
            "EXECUTED",  # статус
            "нет",  # сортировать по дате?
            "нет",  # только рублевые?
            "нет",  # фильтрация по описанию?
        ]
    )
    monkeypatch.setattr(
        "builtins.input",
        lambda *args, **kwargs: next(user_inputs),
    )

    main.main()
    captured = capsys.readouterr()
    out = captured.out

    assert "Для обработки выбран XLSX-файл." in out
    assert "Операций со статусом EXECUTED не найдено." in out
    assert "Не найдено ни одной транзакции, подходящей под ваши условия фильтрации" in out


def test_invalid_status_then_valid(monkeypatch, capsys, fake_modules):
    """
    Сценарий:
    - меню: JSON (1)
    - сначала неправильный статус: XXX (должно выдать сообщение)
    - затем корректный: EXECUTED
    - дальше без сортировки/фильтров
    """
    user_inputs = iter(
        [
            "1",  # пункт меню -> JSON
            "XXX",  # некорректный статус
            "EXECUTED",  # корректный статус
            "нет",  # сортировать по дате?
            "нет",  # только рублевые?
            "нет",  # фильтрация по описанию?
        ]
    )

    def fake_input(*args, **kwargs):
        return next(user_inputs)

    monkeypatch.setattr("builtins.input", fake_input)

    main.main()
    captured = capsys.readouterr()
    out = captured.out

    assert "Статус операции XXX недоступен." in out
    assert "Операции отфильтрованы по статусу EXECUTED" in out
    assert "Всего банковских операций в выборке: 2" in out


def test_invalid_menu_choice(monkeypatch, capsys, fake_modules):
    """
    Некорректный пункт меню -> вывод сообщения и завершение.
    """
    user_inputs = iter(
        [
            "99",  # неправильный пункт меню
        ]
    )
    monkeypatch.setattr(
        "builtins.input",
        lambda *args, **kwargs: next(user_inputs),
    )

    main.main()
    captured = capsys.readouterr()
    out = captured.out

    assert "Некорректный номер меню" in out

    # не должно появляться "Для обработки выбран ..." и т.п.
    assert "Для обработки выбран JSON-файл." not in out
    assert "Для обработки выбран CSV-файл." not in out
    assert "Для обработки выбран XLSX-файл." not in out
