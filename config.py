﻿# -*- coding: utf-8 -*-


token = '163863203:' # токен телеграм-бота
oAuthToken = 'AQAD--Jc4H_-' # токен стафф-апи
#oAuthToken =''

# параметры запросов
apiPath = 'https://s'
mHeaders = {'Authorization': 'OAuth {0}'.format(oAuthToken)}
mParams = {'_pretty': '1', '_one': '1', '_fields': 'phones.number,name,login,cars,accounts,official.is_dismissed'}

# тексты сообщений
errorMsg = 'Не удалось найти номер. Попробуйте на русском без пробелов ("М923КУ777") или без кода страны ("М923КУ")'
welcomeMsg = 'привет! Бот возвращает телефон со стаффа по номеру авто. Раскладка и пробелы не важны. Пример запроса: "М923КУ777"'
mNotPlateMsg = 'Хм! Кажется, это не гос.номер. Длина от 3 од 15 символ и содержит цифры и буквы. Пример запроса: "М 923 КУ 777"'
noPhoneOnStaffMsg = 'Извините, ваш ТЕЛЕФОННЫЙ номер не найден на стаффе. Вам нельзя пользоваться этим ботом. Хотя, может быть я вас просто забыл. Нажмите на значок клавиатуры и на кнопку "Отправить свой номер телефона боту" :)'
RememberMsg = 'Я все еще помню, что вам можно доверять. Посылать номер уже не обязательно'
mGetPhoneMsg = 'Нажмите на кнопку "Отправить свой номер телефона боту". Я проверю, можно ли вам доверять :)'

#прочие параметры
mPhoneWhiteList = ['79263936053',  '79099907689', '79264003309', '79059885836']  # скоро уволюсь, а ботика друзьям показать хочется))
mButtonTitle = 'Отправить свой номер телефона боту'