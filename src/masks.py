def get_mask_card_number(card_number: str) -> str:
    """Функция принимает номер карты, возвращает маскированный номер"""
    masked_card_number = card_number[:6] + "******" + card_number[-4:]
    chunks = [masked_card_number[i : i + 4] for i in range(0, len(masked_card_number), 4)]
    resulting_masked_card_number: str = " ".join(chunks)
    return resulting_masked_card_number


def get_mask_account(account_id: str) -> str:
    """Функция принимает номер счета, возвращает маскированный номер"""
    masked_account_id = "**" + account_id[-4:]
    return masked_account_id
