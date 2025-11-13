import json
import os
from dotenv import load_dotenv
import requests

load_dotenv()
api_key = os.getenv('API_KEY')
headers = {
    "apikey": f"{api_key}"
}
def amount_of_transaction_in_ruble (transaction: dict)-> float:
    """Функция принимает на вход транзакцию и возвращает сумму транзакции (amount) в рублях,
     тип данных — float. Если транзакция была в USD или EUR, происходит обращение
     к внешнему API для получения текущего курса валют и конвертации суммы операции в рубли.
     Для конвертации валюты используется Exchange Rates Data API: https://apilayer.com/exchangerates_data-api.

    """
    amount = transaction.get('operationAmount').get('amount')
    if transaction.get('operationAmount').get('currency').get('code') =='RUB':
        amount_rub = amount
        return amount_rub
    else:
        convert_to ='RUB'
        convert_from = transaction.get('operationAmount').get('currency').get('code')
        url = f'https://api.apilayer.com/exchangerates_data/convert?to={convert_to}&from={convert_from}&amount={amount}'
        response = requests.get(url, headers=headers)
        status_code = response.status_code
        if status_code == 200:
            content = response.text
            content_dict = json.loads(content)
            amount_rub = content_dict.get("result")
        else:
            #print(f"Запрос не был успешным. Возможная причина: {response.reason}")
            amount_rub = 0
    return amount_rub

'''
print(amount_of_transaction_in_ruble({
    "id": 41428829,
    "state": "EXECUTED",
    "date": "2019-07-03T18:35:29.512364",
    "operationAmount": {
      "amount": "8221.37",
      "currency": {
        "name": "USD",
        "code": "USD"
      }
    },
    "description": "Перевод организации",
    "from": "MasterCard 7158300734726758",
    "to": "Счет 35383033474447895560"
  }))

'''