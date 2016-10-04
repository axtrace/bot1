# -*- coding: utf-8 -*-

import requests
import logging
import re

import config
import trans


class NumberIdentifier:
    def __init__(self):
        self.x = 'Hello'

    mHeaders = config.mHeaders
    mParams = config.mParams
    mPath = config.apiPath


    def checkTelegramLogin(self, login):
        result = {'code': -1, 'name': ''}
        # проверим, что логин есть на стаффе
        mTempParams = self.mParams.copy()
        mTempParams['accounts.value'] = login
        r = requests.get(self.mPath, params=mTempParams, headers=self.mHeaders)
        if 'error_message' not in r.text:
            mTelegramAccount = self.getTelegramAccount(r.json()['accounts'])
            if mTelegramAccount['value'] == login:
                result = {'code': 0, 'name': r.json()['name']['first']['ru']}
        return result


    def checkSendersPhone(self, phonestring):
        # проверим, что телефон есть на стаффе
        result = {'code': -1, 'name': ''}
        mTempParams = self.mParams.copy()
        mTempParams['_query'] = u"phones.number==regex('" + self.formatPhone(phonestring) + "')"
        r = requests.get(self.mPath, params=mTempParams, headers=self.mHeaders)
        if 'error_message' not in r.text:
            result = {'code': 0, 'name': r.json()['name']['first']['ru']}
        return result


    def formatPhone(self, phonestring):
        # конвертим телефон в regex формат
        result = ''
        spaceIndex = (2, 5, 8, 10)
        if phonestring[0] == '3':
            spaceIndex = (4, 6, 9, 11)  # под украинский формат
        for index, char in enumerate(phonestring, 1):
            if index in spaceIndex:
                result += '.*'
            result += char
        result = '.*' + result + '.*'
        return result


    def findPhoneNumber(self, platestring, k):
        # Перебираем разные варианты номера авто (по алфативу, формату пробелов, регистру)
        tr = trans.Translator()
        result = self.getPhoneNumberByPlate(tr.mAddRegPlate(platestring),0)
        result['req'] = platestring
        return result


    def getPhoneNumberByPlate(self, platestring, k):
        # запрашивает k-й номер телефона по номеру авто
        # планирую потом расширить до всех номеров, но пока лень разбираться со структурами данных

        # Задаем дефолтовый резалт, который потом пытаемся менять
        result = {'code': -1, 'phone_number': '', 'name': '', 'surname': '', 'login': '', 'req': platestring, 'is_dismissed': True}
        mTempParams = self.mParams.copy()
        #mTempParams['cars.plate'] = platestring
        mTempParams['_query'] = u"cars.plate==regex('" + platestring + "')"
        logging.debug('\t\t\tgetPhoneNumberByPlate(). Finding {0}'.format(platestring))
        r = requests.get(self.mPath, params=mTempParams, headers=self.mHeaders)
        r.encoding = 'utf-8'

        # если в ответе не было сообщения об ошибке, считаем, что номер нашли и кладем данные в резалт
        if 'error_message' not in r.text:
            result['code'] = 0
            result['phone_number'] = r.json()['phones'][k]['number']
            result['name'] = r.json()['name']['first']['ru']
            result['surname'] = r.json()['name']['last']['ru']
            result['login'] = r.json()['login']
            result['model'] = self.getModelByPlate(r.json()['cars'], platestring)['model']
            result['plate'] = self.getModelByPlate(r.json()['cars'], platestring)['plate']
            result['is_dismissed'] = r.json()['official']['is_dismissed']
        return result

    def getModelByPlate(self, cars, plate):
        mCar = {'model': '', 'plate': ''}
        for car in cars:
            if re.search(plate, car['plate']):
                mCar = {'model': car['model'], 'plate': car['plate']}
        return mCar


    def getTelegramAccount(self, accounts):
        mAcount = {'type': '', 'value': ''}
        for value in accounts:
            if re.search('telegram', value['type']):
                mAcount = {'type': value['type'], 'value': value['value']}
        return mAcount