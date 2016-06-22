# -*- coding: utf-8 -*-
# возвращает номер телефона по номеру авто. Номер авто надо вводить полностью (ограничение апи стаффа).
# Для номера нет разницы между кириллицей и латиницей.
# Планы: возвращать не номер, а писать сообщение владельцу номера. То есть анонимизировать вторую сторону.
# Еще здорово прилипить распознавание номера авто по фото, чтобы убрать ручной ввод.


import config
import getNumber
import telebot
from telebot import types

bot = telebot.TeleBot(config.token)
numId = getNumber.NumberIdentifier()


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('1', '2')  # Имена кнопок
    msg = bot.reply_to(message, 'Test text', reply_markup=markup)
    bot.register_next_step_handler(msg, process_step)
#to-do: запилить реквест номера телефона отправителя и пробивку его на стаффе


def process_step(message):
    print(message.text)


@bot.message_handler(content_types=["text"])
def send_phone_number(message):

    if len(message.text) > 15:
        bot.send_message(message.chat.id, config.mToLongMsg)
    else:
        mMsg = form_msg(numId.findPhoneNumber(message.text, 0))
        bot.send_message(message.chat.id, mMsg)


def form_msg(mData):
    mMsg = config.errorMsg
    if mData['code'] == -1:
        mMsg = 'Номер: ' + mData['req'] + '. ' + config.errorMsg
    if mData['code'] == 0:
        mMsg = mData['req'] + '.\n' + mData['phone_number'] + '. ' + mData['name']
    return mMsg

if __name__ == '__main__':
    bot.polling(none_stop=True)