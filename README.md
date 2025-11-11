# Bank_Widget
Приложение создано для работы с банковскими данными и операциями клиента. На данном этапе может маскировать номера карты и счета, сортировать операции по дате и статусу, генерировать номер карты, а также логировать работу функций с помощью декоратора lig. Находится в разработке

## Содержание
- [Использование](#Использование)
- [Разработка](#разработка)
- [Тестирование](#тестирование)
- [To do](#to-do)
- [Команда проекта](#команда-проекта)

## Использование
### Установка
1 Clone repository
`git clone git@github.com:Farkhad96/HomeWorkProject.git`

`cd HomeworkProject`

2 Create virtual environment
`python3.13 -m venv .venv`

`source .venv/bin/activate`

3 Install dependencies

`pip install poetry`

`poetry install`
### Примеры использования функций модуля generator.py
```
usd_transactions = filter_by_currency(transactions, "USD")
for _ in range(2):
    print(next(usd_transactions))

>>> {
          "id": 939719570,
          "state": "EXECUTED",
          "date": "2018-06-30T02:08:58.425572",
          "operationAmount": {
              "amount": "9824.07",
              "currency": {
                  "name": "USD",
                  "code": "USD"
              }
          },
          "description": "Перевод организации",
          "from": "Счет 75106830613657916952",
          "to": "Счет 11776614605963066702"
      }
      {
              "id": 142264268,
              "state": "EXECUTED",
              "date": "2019-04-04T23:20:05.206878",
              "operationAmount": {
                  "amount": "79114.93",
                  "currency": {
                      "name": "USD",
                      "code": "USD"
                  }
              },
              "description": "Перевод со счета на счет",
              "from": "Счет 19708645243227258542",
              "to": "Счет 75651667383060284188"
       }
```
```commandline
for card_number in card_number_generator(1, 5):
    print(card_number)

>>> 0000 0000 0000 0001
    0000 0000 0000 0002
    0000 0000 0000 0003
    0000 0000 0000 0004
    0000 0000 0000 0005
```
```commandline
descriptions = transaction_descriptions(transactions)
for _ in range(5):
    print(next(descriptions))

>>> Перевод организации
    Перевод со счета на счет
    Перевод со счета на счет
    Перевод с карты на карту
    Перевод организации
```
## Разработка

### Требования
Для установки и запуска проекта требуется python 3.13 и выше

## Тестирование
Данный проект протестирован юнит-тестами Pytest. Для запуска выполните команду
`pytest --cov`

## FAQ 
Данный раздел пока пустой, так как не было задано вопросов
### Зачем вы разработали этот проект?
Чтобы был.

## To do
- [x] Добавить крутое README
- [ ] Всё переписать

## Команда проекта

- [Фархад Зайнуллин](https://t.me/madflyzero) — Back-End Engineer

## Источники
