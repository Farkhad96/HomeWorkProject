# main.py
import src.generators
import src.processing
import src.utils
import src.widget


def main():
    print(
        """Привет! Добро пожаловать в программу работы с банковскими транзакциями.
Выберите необходимый пункт меню:
 1. Получить информацию о транзакциях из JSON-файла
 2. Получить информацию о транзакциях из CSV-файла
 3. Получить информацию о транзакциях из XLSX-файла"""
    )
    transaction_data = []
    user_input = int(input("Введите номер пункта меню: "))

    if user_input in [1, 2, 3]:
        if user_input == 1:
            print("Для обработки выбран JSON-файл.")
            transaction_data = src.utils.load_transactions("data/operations.json")
        elif user_input == 2:
            print("Для обработки выбран CSV-файл.")
            transaction_data = src.utils.load_transactions("data/transactions.csv")
        elif user_input == 3:
            print("Для обработки выбран XLSX-файл.")
            transaction_data = src.utils.load_transactions("data/transactions_excel.xlsx")
    else:
        print("Некорректный номер меню")
        return

    filtered_transaction_data = []

    while True:
        print(
            """Введите статус, по которому необходимо выполнить фильтрацию.
Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING"""
        )
        state = input().strip()
        if state.upper() in ["EXECUTED", "CANCELED", "PENDING"]:
            filtered_transaction_data = src.processing.filter_by_state(transaction_data, state)
            if filtered_transaction_data:
                print(f"Операции отфильтрованы по статусу {state}")
                break
            else:
                print(f"Операций со статусом {state} не найдено.")
                break
        else:
            print(f"Статус операции {state} недоступен.")
            continue

    sorted_transactions = filtered_transaction_data

    while True:
        print("Отсортировать операции по дате? Да/Нет")
        answer_sort_by_date = input().strip()
        if answer_sort_by_date.upper() == "ДА":
            while True:
                print("Отсортировать по возрастанию или по убыванию? по возрастанию/по убыванию")
                answer_descending = input().strip()
                if answer_descending.upper() == "ПО УБЫВАНИЮ":
                    sorted_transactions = src.processing.sort_by_date(filtered_transaction_data, True)
                    break
                elif answer_descending.upper() == "ПО ВОЗРАСТАНИЮ":
                    sorted_transactions = src.processing.sort_by_date(filtered_transaction_data, False)
                    break
                else:
                    print(f"Ответ {answer_descending} не корректен")
                    continue
            break
        elif answer_sort_by_date.upper() == "НЕТ":
            sorted_transactions = filtered_transaction_data
            break
        else:
            print(f"Ответ {answer_sort_by_date} не корректен")
            continue

    filtered_transactions = sorted_transactions

    while True:
        print("Выводить только рублевые транзакции? Да/Нет")
        answer_currency_rub = input().strip()
        if answer_currency_rub.upper() == "ДА":
            filtered_transactions = list(src.generators.filter_by_currency(sorted_transactions, "RUB"))
            break
        elif answer_currency_rub.upper() == "НЕТ":
            filtered_transactions = sorted_transactions
            break
        else:
            print(f"Ответ {answer_currency_rub} не корректен")
            continue

    description_filtered_transactions = filtered_transactions

    while True:
        print("Отфильтровать список транзакций по определенному слову в описании? Да/Нет")
        answer_description = input().strip()
        if answer_description.upper() == "ДА":
            print("Введите слово для поиска")
            answer_description_ = input().strip()
            description_filtered_transactions = src.processing.process_bank_search(
                description_filtered_transactions,
                answer_description_,
            )
            break
        elif answer_description.upper() == "НЕТ":
            description_filtered_transactions = filtered_transactions
            break
        else:
            print(f"Ответ {answer_description} не корректен")
            continue

    if description_filtered_transactions:
        print("Распечатываю итоговый список транзакций...")
        print(f"Всего банковских операций в выборке: {len(description_filtered_transactions)}")
        for transaction in description_filtered_transactions:
            print(src.widget.get_date(transaction.get("date")), transaction.get("description"))
            if transaction.get("from"):
                print(
                    src.widget.mask_account_card(transaction.get("from")),
                    "->",
                    src.widget.mask_account_card(transaction.get("to")),
                )
            else:
                print(src.widget.mask_account_card(transaction.get("to")))
            print("Сумма:", transaction.get("operationAmount").get("amount"))
    else:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")


if __name__ == "__main__":
    main()
