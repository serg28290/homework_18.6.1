import requests
import json
from config import keys


class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base and quote in keys:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}.')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Валюты {quote} нет в списке\nдоступных для конвертации')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Валюты {base} нет в списке\nдоступных для конвертации')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Количество {amount} является некорректным значением')
            
        req = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = round(json.loads(req.content)[keys[base]] * amount, 2)
        return total_base
      
