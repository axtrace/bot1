# -*- coding: utf-8 -*-
# Возвращает первый номер телефона со стаффа по номеру авто. Номер авто надо вводить полностью (ограничение апи стаффа).
# Авторизация идет по принципу "телефон есть на стафф".
# Для номер не имеет значение: большие или маленькие буквы, кириллица или латиница, пробелы между буквами и цифрами.
# sofinma@: В пианиста просьба не стрелять, писал код как мог. Это моя первая программа на python.
# Кривизну некоторых решений вижу.
# Большое спасибо varkasha@ за консультации и ответы на вопросы "а как это вообще"

import telebot
from telebot import types
import logging
import re

import config
import getNumber

bot = telebot.TeleBot(config.token)
numId = getNumber.NumberIdentifier()
mChatidList = []
mPhoneWhiteList = config.mPhoneWhiteList.copy()
mButtonTitle = config.mButtonTitle
logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s',
                    level = logging.DEBUG, filename = u'botlog.log')

@bot.message_handler(commands=['start'])
def start_handler(message):
    # Получаем номер телефона от пользователя
    logging.debug('start_handler. ChatId: {0}. Get message: {1}'.format(message.chat.id, message.text))
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    batton = types.KeyboardButton(mButtonTitle, request_contact=True)
    markup.add(batton)
    msg = bot.reply_to(message, config.mGetPhoneMsg, reply_markup=markup)

@bot.message_handler(content_types=["contact"])
def check_chatid(message):
    if message.chat.id in mChatidList:
        bot.send_message(message.chat.id, config.RememberMsg)
    else:
        check_phone_number(message)


def check_phone_number(message):    
    mCheckRes = {'code': 0, 'name': 'Добрый человек'}
    mPhoneNumber = re.sub(r'(\s+)?[+]?[-]?', '', message.contact.phone_number)
    if (mPhoneNumber not in mPhoneWhiteList):
        logging.debug('check_phone_number. Chatid {0} NOT in mPhoneWhiteList'.format(message.chat.id))
        mCheckRes = numId.checkSendersPhone(mPhoneNumber)
    if (mCheckRes['code'] == 0):
        # добавляю в список пользователей
        mMsg = mCheckRes['name'] + ", " + config.welcomeMsg
        mChatidList.append(message.chat.id)
        logging.debug('check_phone_number. Add Chatid {0} to mPhoneWhiteList'.format(message.chat.id))
    else:
        mMsg = config.noPhoneOnStaffMsg
    bot.send_message(message.chat.id, mMsg)
    logging.debug('check_phone_number.  ChatId: {0}. Send message: {1}'.format(message.chat.id, mMsg))

@bot.message_handler(content_types=["text"])
def send_phone_number(message):
    if (len(message.text) > 15) \
            or (not message.text.replace(' ', '').isalnum()
                or message.text.replace(' ', '').isdigit()
                or message.text.replace(' ', '').isalpha()):
        bot.send_message(message.chat.id, config.mNotPlateMsg)
    else:
        if message.chat.id in mChatidList:
            mMsg = form_msg(numId.findPhoneNumber(message.text, 0))
        else:
            mMsg = config.noPhoneOnStaffMsg
        bot.send_message(message.chat.id, mMsg)
        logging.debug('send_phone_number.  ChatId: {0}. Send message: {1}'.format(message.chat.id, mMsg))

def form_msg(mData):
    mMsg = config.errorMsg
    if mData['code'] == -1:
        mMsg = mData['req'] + '. ' + config.errorMsg
    if mData['code'] == 0:
        mMsg = mData['plate'] + '. ' + mData['model'] + '\n' + mData['phone_number'] + '\n ' + mData['login'] + '@. ' + mData['name'] + ' ' + mData['surname']
    return mMsg

if __name__ == '__main__':
    bot.polling(none_stop=True)