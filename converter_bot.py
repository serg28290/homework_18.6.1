import telebot
from config import keys, TOKEN
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help_(message: telebot.types.Message):
    text = 'Чтобы сконверитровать валюту, введите команду боту в следующем формате через пробел:\n' \
           '<имя валюты>\n' \
           '<в какую валюту перевести>\n' \
           '<количество переводимой валюты>\n' \
           'Для просмотра списка доступных валют, нажмите на ссылку\n' \
           '/values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        val = message.text.lower().split(' ')
        if len(val) != 3:
            raise APIException('Слишком много параметров')
        quote, base, amount = val
        total_base = CryptoConverter.convert(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'{amount} {keys[quote]} в {keys[base]} = {total_base} {keys[base]}'
        bot.send_message(message.chat.id, text)


bot.polling()
