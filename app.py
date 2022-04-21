import telebot
from config import TOKEN, keys
from extensions import ConvertionException, Cryptoconverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start','help'])
def send_welcome(message):
	text = 'For currency exchange rate, type:\n<currency-1> \
<currency-2> <amount of currency-1>\nAvailable currencies: /values \
\nExample:\n usd rub 1 \n eur rub 1'
	bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
	text = 'Available currencies:'
	for key in keys.keys():
		text = '\n' .join((text, key,))
	bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
	try:
		values = message.text.split(' ')
		
		if len(values) != 3:
			raise ConvertionException('Shall be: currency-1 currency-2 amount\n or type /help')

		base, quote, amount = values
		total_base = Cryptoconverter.get_price(base, quote, amount)
	except ConvertionException as e:
		bot.reply_to(message, f'User error.\n{e}')
	except Exception as e:
		bot.reply_to(message, f'Cannot handle instruction\n{e}')
	else:
		text = f'price {amount} {base} in {quote} = {total_base} {keys[quote]}'
		bot.send_message(message.chat.id, text)

bot.infinity_polling()
