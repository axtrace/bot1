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

    def checkSendersPhone(self, phonestring):
        # проверим, что телефон есть на стаффе
        result = {'code': -1, 'name': ''}
        mTempParams = self.mParams.copy()
        mTempParams['phones.number'] = r'+' + phonestring
        r = requests.get(self.mPath, params=mTempParams, headers=self.mHeaders)
        # номер не нашли, пробуем искать в форматированном фиде
        if 'error_message' in r.text:
            mTempParams['phones.number'] = r'+' + self.formatPhone(phonestring)
            r = requests.get(self.mPath, params=mTempParams, headers=self.mHeaders)
        # если в ответе не было сообщения об ошибке, считаем, что номер нашли
        if 'error_message' not in r.text:
            result = {'code': 0, 'name': r.json()['name']['first']['ru']}
        return result


    def formatPhone(self, phonestring):
        # конвертим телефон в международный формат +7 (926) 111-11-11 или +380 (50) 222-22-22.
        # На стаффе встречаются и другие форматы, но они исчезающе редки. Примеры: 8-903-111-11-11, 8(926)111-11-11
        result = ''
        spaceIndex = (2, 5)
        hypIndex = (8, 10)
        if phonestring[0] == '3':
            spaceIndex = (4, 6)  # под украинский формат
            hypIndex = (9, 11)
        wasOpenBracket = False
        for index, char in enumerate(phonestring, 1):
            if index in spaceIndex:
                if wasOpenBracket:
                    result += ') '
                    wasOpenBracket = False
                else:
                    result += ' ('
                    wasOpenBracket = True
            else:
                if index in hypIndex:
                    result += '-'
            result += char
        return result


    def findPhoneNumber(self, platestring, k):
        # Перебираем разные варианты номера авто (по алфативу, формату пробелов, регистру)
        result = self.findPhoneNumberByLangModeRegister(platestring, k)
        result['req'] = platestring
        return result

    def findPhoneNumberByLangModeRegister(self, platestring, k):
        # Перебираем варианты алфавитов для поиска. Как есть, русский, латиница.
        # Если не получилось, пробуем тоже самое, но без пробелов
        tr = trans.Translator()
        result = {'code': -1, 'req': platestring}
        for TrDir in ('En2Ru', 'Ru2En', 'as-is'):
            logging.debug('findPhoneNumberByLangModeRegister(). Finding {0}. Direction: {1}'.format(platestring, TrDir))
            mText = tr.transliterate(platestring, TrDir)
            result = self.findPhoneNubmerByModeAndRegister(mText, k)
            if result['code'] == 0:
                return result
        return result

    def findPhoneNubmerByModeAndRegister(self, platestring, k):
        # Перебираем варианты пробелов в гос.номере. Как есть, авто, без пробелов и мото
        tr = trans.Translator()
        mNum = {'code': -1, 'req': platestring}
        for mode in ('auto', 'no', 'as-is', 'moto'):
            logging.debug('\tfindPhoneNubmerByModeAndRegister(). Finding {0}. Format: {1}'.format(platestring, mode))
            mNum = self.findPhoneNumberByRegister(tr.mSpaceMode(platestring,mode), k)
            if mNum['code'] == 0:
                return mNum
        return mNum

    def findPhoneNumberByRegister(self, platestring, k):
        # Сначала ищем как есть, затем в верхнем регистре, затем в нижнем
        logging.debug('\t\tfindPhoneNumberByRegister(). Finding {0}. Registr as-is'.format(platestring))
        mNum = self.getPhoneNumberByPlate(platestring, k)
        if mNum['code'] == -1:
            logging.debug('\t\tfindPhoneNumberByRegister(). Finding {0}. Registr upper'.format(platestring.upper()))
            mNum = self.getPhoneNumberByPlate(platestring.upper(), k)
        if mNum['code'] == -1:
            logging.debug('\t\tfindPhoneNumberByRegister(). Finding {0}. Registr lower'.format(platestring.lower()))
            mNum = self.getPhoneNumberByPlate(platestring.lower(), k)
        return mNum

    def getPhoneNumberByPlate(self, platestring, k):
        # запрашивает k-й номер телефона по номеру авто
        # планирую потом расширить до всех номеров, но пока лень разбираться со структурами данных

        # Задаем дефолтовый резалт, который потом пытаемся менять
        result = {'code': -1, 'phone_number': '', 'name': '', 'surname': '', 'login': '', 'req': platestring}
        mTempParams = self.mParams.copy()
        mTempParams['cars.plate'] = platestring
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
            result['model'] = self.getModelByPlate(r.json()['cars'], platestring)
            result['plate'] = platestring
        return result

    def getModelByPlate(self, cars, plate):
        model = ""
        for car in cars:
            if car['plate'] == plate:
                model = car['model']
        return model
