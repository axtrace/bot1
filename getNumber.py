# -*- coding: utf-8 -*-

import requests
import config
import trans


class NumberIdentifier:
    def __init__(self):
        self.x = 'Hello'

    mHeaders = config.mHeaders
    mParams = config.mParams
    mPath = config.apiPath

    def getPhoneNumberByPlate(self, platestring, k):
        # запрашивает k-й номер телефона по номеру авто
        # планирую потом расширить до всех номеров, но пока лень разбираться со структурами данных

        # Задаем дефолтовый резалт, который потом пытаемся менять
        result = {'code': -1, 'phone_number': '', 'name': ''}

        self.mParams['cars.plate'] = platestring
        r = requests.get(self.mPath, params=self.mParams, headers=self.mHeaders)
        r.encoding = 'utf-8'

        # если в ответе не было сообщения об ошибке, считаем, что номер нашли и кладем данные в резалт
        if 'error_message' not in r.text:
            result = {'code': 0, 'phone_number': r.json()['phones'][k]['number'], 'name': r.json()['name']['first']['ru']}

        return result

    def findPhoneNumber(self, platestring, k):
        # перебирает разные варианты номера авто пока не найдет телефон

        # Попробуем поискать сначала на кириллице, а затем - на латинице
        result = self.findPhoneNumberLang(platestring, k, 'En2Ru')
        if result['code'] == -1:
            result = self.findPhoneNumberLang(platestring, k, 'Ru2En')

        return result

    def findPhoneNumberLang(self, platestring, k, TrDir):

        tr = trans.Translator()

        # Просто приводим к нужному алфавиту и ищем. Если не получилось, пробуем без пробелов
        mText = tr.transliterate(platestring, TrDir)
        mNum = self.getPhoneNumberByPlate(mText, k)

        if mNum['code'] == -1:
            mNum = self.getPhoneNumberByPlate(mText.replace(' ', ''), k)

        mNum['req'] = mText

        return mNum