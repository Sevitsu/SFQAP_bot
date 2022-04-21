import requests
import json
from config import keys

class ConvertionException(Exception):
	pass

class Cryptoconverter:
	@staticmethod
	def get_price(base: str, quote: str, amount: str):
		if base == quote:
			raise ConvertionException(f'The same currency unacceptable {quote}')

		try:
			base_ticker = keys[base]
		except KeyError:
			raise ConvertionException(f'Incorrect currency {base}')
	
		try:
			quote_ticker = keys[quote]
		except KeyError:
			raise ConvertionException(f'Incorrect currency {quote}')

		try:
			amount = float(amount)
		except ValueError:
			raise ConvertionException(f'Incorrect amount {amount}')
			
		r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
		total_base = json.loads(r.content)[keys[quote]]

		return total_base
