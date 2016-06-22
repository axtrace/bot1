# -*- coding: utf-8 -*-


token = 'xxx'
oAuthToken = 'xxx'

apiPath = 'xxx'
mHeaders = {'Authorization': oAuthToken}
mParams = {'_pretty': '1', '_one': '1', '_fields': 'phones.number,name,login,cars'}

errorMsg = 'Не удалось найти номер. Попробуйте на русском, через проблемы. Пример: "М 923 КУ 777"'
welcomeMsg = 'Бот возвращает телефон по номеру авто. Пример запроса: "М 923 КУ 777"'
mToLongMsg = 'Слишком длинное сообщение. Думаю, это не номер авто. Пример запроса: "М 923 КУ 777"'