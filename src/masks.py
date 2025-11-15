import logging

logger = logging.getLogger("masks")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("../logs/masks.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s : %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Функция принимает номер карты, возвращает маскированный номер"""
    logger.info(f"Функция get_mask_card_number приняла на вход {card_number}")
    try:
        if len(card_number) == 16 and card_number.isdigit():
            masked_card_number = card_number[:6] + "******" + card_number[-4:]
            chunks = [masked_card_number[i : i + 4] for i in range(0, len(masked_card_number), 4)]
            resulting_masked_card_number: str = " ".join(chunks)
            logger.info(f"Функция возвращает {resulting_masked_card_number}")
            return resulting_masked_card_number
    except Exception as ex:
        logger.info(f"Возникла ошибка {ex}")
        return "Неправильно набран номер"
    return "Неправильно набран номер"


def get_mask_account(account_id: str) -> str:
    """Функция принимает номер счета, возвращает маскированный номер"""
    logger.info(f"Функция get_mask_account приняла на вход {account_id}")
    try:
        if len(account_id) == 20 and account_id.isdigit():
            masked_account_id = "**" + account_id[-4:]
            logger.info(f"Функция возвращает {masked_account_id}")
            return masked_account_id
        return "Неправильно набран номер"
    except Exception as ex:
        logger.info(f"Возникла ошибка {ex}")
        return "Неправильно набран номер"
