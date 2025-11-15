import json

from src.utils import load_transactions


def test_file_not_found():
    # Test case for file not found
    result = load_transactions("non_existent_file.json")
    assert result == []


def test_empty_file(tmp_path):
    # Test case for empty file using pytest's tmp_path fixture
    empty_file = tmp_path / "empty_file.json"
    empty_file.write_text("")
    result = load_transactions(str(empty_file))
    assert result == []


def test_invalid_json(tmp_path):
    # Test case for invalid JSON
    invalid_file = tmp_path / "invalid_file.json"
    invalid_file.write_text("This is not JSON")
    result = load_transactions(str(invalid_file))
    assert result == []


def test_json_not_list(tmp_path):
    # Test case where JSON is not a list
    not_a_list_file = tmp_path / "not_a_list.json"
    not_a_list_file.write_text('{"key": "value"}')
    result = load_transactions(str(not_a_list_file))
    assert result == []


def test_valid_json(tmp_path):
    # Test case for valid JSON list
    transactions = [{"id": 1, "amount": 100.0, "currency": "USD"}, {"id": 2, "amount": 200.0, "currency": "EUR"}]
    valid_file = tmp_path / "valid_file.json"
    valid_file.write_text(json.dumps(transactions, ensure_ascii=False))
    result = load_transactions(str(valid_file))
    assert result == transactions
