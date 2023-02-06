import telebot
from config import keys, TOKEN
from extensions import APIException, CryptoConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = f'Здравствуйте {message.chat.username}! \n\nЯ помогу вам конвертировать валюту.\n\nДля этого введите команду в следующем формате: \
\n\n<Имя исходной валюты> <В какую валюту перевести> <Количество переводимой валюты>\n\nПример: Доллар рубль 100\n\nУвидеть список всех доступных валют /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные для ковертации валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Не верное количество параметров\nВведите команду в следующем формате: \
\n<Имя исходной валюты> <В какую валюту перевести> <Количество переводимой валюты валюты>\nУвидеть список всех доступных валют /values ')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
