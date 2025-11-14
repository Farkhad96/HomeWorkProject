import importlib
import json
from unittest.mock import Mock, patch


def reload_external_api(monkeypatch):
    """
    Вспомогательная функция:
    - подменяет переменную окружения API_KEY;
    - пере-загружает модуль external_api, чтобы headers пересоздались.
    """
    monkeypatch.setenv("API_KEY", "test-api-key")

    import src.external_api

    importlib.reload(src.external_api)
    return src.external_api


def test_amount_in_ruble_does_not_call_api(monkeypatch):
    """
    Если валюта уже в RUB — внешний API вызываться не должен,
    а функция просто возвращает amount.
    """
    external_api = reload_external_api(monkeypatch)

    transaction = {
        "operationAmount": {
            "amount": 1000.0,
            "currency": {"code": "RUB", "name": "Рубли"},
        }
    }

    with patch.object(external_api, "requests") as mock_requests:
        result = external_api.amount_of_transaction_in_ruble(transaction)

    assert result == 1000.0
    mock_requests.get.assert_not_called()


def test_amount_in_usd_success(monkeypatch):
    """
    Если валюта USD и API вернул 200 + result — функция должна
    вернуть значение result (в рублях) и корректно дернуть requests.get.
    """
    external_api = reload_external_api(monkeypatch)

    transaction = {
        "operationAmount": {
            "amount": 10.0,
            "currency": {"code": "USD", "name": "Доллар США"},
        }
    }

    fake_response = Mock()
    fake_response.status_code = 200
    fake_response.text = json.dumps({"result": 987.65})

    with patch.object(external_api.requests, "get", return_value=fake_response) as mock_get:
        result = external_api.amount_of_transaction_in_ruble(transaction)

    assert result == 987.65

    # проверим, что запрос был ровно один
    mock_get.assert_called_once()

    # проверим, что URL сформирован как ожидается (грубо, без фанатизма)
    called_url = mock_get.call_args[0][0]
    assert "to=RUB" in called_url
    assert "from=USD" in called_url
    assert "amount=10.0" in called_url

    # и что передаются headers с API ключом
    called_kwargs = mock_get.call_args[1]
    assert "headers" in called_kwargs
    assert called_kwargs["headers"].get("apikey") == "test-api-key"


def test_amount_in_eur_api_failure_returns_zero(monkeypatch):
    """
    Если валюта не RUB, но API вернул статус != 200,
    текущая реализация возвращает 0 — это и проверяем.
    """
    external_api = reload_external_api(monkeypatch)

    transaction = {
        "operationAmount": {
            "amount": 50.0,
            "currency": {"code": "EUR", "name": "Евро"},
        }
    }

    fake_response = Mock()
    fake_response.status_code = 500
    fake_response.text = "Internal error"
    fake_response.reason = "Internal Server Error"

    with patch.object(external_api.requests, "get", return_value=fake_response) as mock_get:
        result = external_api.amount_of_transaction_in_ruble(transaction)

    assert result == 0
    mock_get.assert_called_once()
