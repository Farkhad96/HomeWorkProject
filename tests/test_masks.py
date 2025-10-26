import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "card_number, masked_number",
    [
        ("7000792289606361", "7000 79** **** 6361"),
        ("1234567890123", "Неправильно набран номер"),
        ("", "Неправильно набран номер"),
    ],
)
def test_get_mask_card_number(card_number: str, masked_number: str) -> None:
    assert get_mask_card_number(card_number) == masked_number


@pytest.mark.parametrize(
    "account_number, masked_account_number",
    [
        ("73654108430135874305", "**4305"),
        ("", "Неправильно набран номер"),
        ("1234567890123", "Неправильно набран номер"),
    ],
)
def test_get_mask_account(account_number: str, masked_account_number: str) -> None:
    assert get_mask_account(account_number) == masked_account_number


# def test_error_masks_card_error()->None:
#     with pytest.raises(TypeError):
#         get_mask_card_number(123456)
#
#
# def test_error_masks_account_error()->None:
#     with pytest.raises(TypeError):
#         get_mask_account(123456)
