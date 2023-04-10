# вывод курсов

import json
import telebot
import requests

token = '5964559637:AAFzIyiMImcue0INMap0PbpmG9X1mrqxXm0'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def hello_Message(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['USD', 'EUR', 'CNY']
    for i in buttons:
        markup.add(telebot.types.KeyboardButton(i))

    bot.send_message(message.chat.id, f'Привет! Выбери интересующую валюту, {message.from_user.first_name}', reply_markup=markup)


@bot.message_handler(content_types='text')
def text(message):
    allowed_currencies = ['USD', 'EUR', 'CNY']
    if message.text in allowed_currencies:
        res = get_Course(message.text)
        bot.send_message(message.chat.id, res)
    else:
        bot.send_message(message.chat.id, 'Я так не умею')


def get_Course(cur):
    try:
        response = requests.get('https://www.nbrb.by/api/exrates/rates/' + cur + '?parammode=2')
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        return f"Error: {error}"
    except requests.exceptions.RequestException as error:
        return f"Error: {error}"
    else:
        data = json.loads(response.text)
        cur = data['Cur_OfficialRate']
        amount = data['Cur_Scale']
        return f"{cur} к {amount} бел.руб."


bot.polling()
