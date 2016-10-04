# -*- coding: utf-8 -*-

class Translator:
    # приводит все буквы к заглавным кириллическим или заглавным латинским, чтобы поискать и так и так
    def __init__(self):
        self.x = 'Hello'

    def transliterate(self, string, direction):
        match_letters_Ru2En = {
            u'А': u'A',
            u'В': u'B',
            u'Е': u'E',
            u'К': u'K',
            u'М': u'M',
            u'Н': u'H',
            u'О': u'O',
            u'Р': u'P',
            u'С': u'C',
            u'Т': u'T',
            u'У': u'Y',
            u'Х': u'X',
            u'а': u'a',
            u'в': u'b',
            u'е': u'e',
            u'к': u'k',
            u'м': u'm',
            u'н': u'h',
            u'о': u'o',
            u'р': u'p',
            u'с': u'c',
            u'т': u't',
            u'у': u'y',
            u'х': u'x'
        }
        match_letters_En2Ru = {
            u'a': u'а',
            u'b': u'в',
            u'e': u'е',
            u'k': u'к',
            u'm': u'м',
            u'h': u'н',
            u'o': u'о',
            u'p': u'р',
            u'c': u'с',
            u't': u'т',
            u'y': u'у',
            u'x': u'х',
            u'A': u'А',
            u'B': u'В',
            u'E': u'Е',
            u'K': u'К',
            u'M': u'М',
            u'H': u'Н',
            u'O': u'О',
            u'P': u'Р',
            u'C': u'С',
            u'T': u'Т',
            u'Y': u'У',
            u'X': u'Х'
        }
        match_letters = match_letters_En2Ru
        translit_string = u""
        if direction == 'as-is':
            translit_string = string
        else:
            if direction == 'Ru2En':
                match_letters = match_letters_Ru2En
            for index, char in enumerate(string, 1):
                repl = match_letters.get(char)
                if not repl:
                    repl = char
                translit_string += repl
        return translit_string

    def mSpaceMode(self, mString, mode='auto'):
        # форматирует номер под номер авто или номер мотоцикла или вообще без пробелов
        if mode == 'as-is':
            result = mString
        else:
            mStringTrimed = mString.replace(' ', '')
            spaceIndex = {2, 5, 7}  # if mode == 'auto'
            result = u''
            if mode == 'no':
                result = mStringTrimed
            else:
                if mode == 'moto':
                    spaceIndex = {5, 7}  # для форматирования под мото-номер
                for index, char in enumerate(mStringTrimed, 1):
                    if index in spaceIndex:
                        result += ' '
                    result += char
        return result
