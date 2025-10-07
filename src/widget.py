from datetime import datetime


def mask_account_card(card_account_number: str) -> str:
    """Функция принимает номер карты или номер счета, возвращает маскированный номер"""
    if card_account_number[:4] == "Счет":
        account_id = card_account_number[4:]
        masked_account_id = "Счет **" + account_id[-4:]
        return masked_account_id
    else:
        card_number = card_account_number[-16:]
        masked_card_number = card_number[:6] + "******" + card_number[-4:]
        chunks = [masked_card_number[i : i + 4] for i in range(0, len(masked_card_number), 4)]
        resulting_masked_card_number: str = card_account_number[:-16] + " ".join(chunks)
        return resulting_masked_card_number


def get_date(date_str: str) -> str:
    """Функция принимает дату в формате ISO, возвращает дату в формате дд.мм.гг"""
    dt = datetime.fromisoformat(date_str)
    return dt.strftime("%d.%m.%Y")
