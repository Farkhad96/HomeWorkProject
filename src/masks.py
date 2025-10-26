def get_mask_card_number(card_number: str) -> str:
    """Функция принимает номер карты, возвращает маскированный номер"""
    if len(card_number) == 16 and card_number.isdigit():
        masked_card_number = card_number[:6] + "******" + card_number[-4:]
        chunks = [masked_card_number[i : i + 4] for i in range(0, len(masked_card_number), 4)]
        resulting_masked_card_number: str = " ".join(chunks)
        return resulting_masked_card_number
    return "Неправильно набран номер"


def get_mask_account(account_id: str) -> str:
    """Функция принимает номер счета, возвращает маскированный номер"""
    if len(account_id) == 20 and account_id.isdigit():
        masked_account_id = "**" + account_id[-4:]
        return masked_account_id
    return "Неправильно набран номер"
