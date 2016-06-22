# -*- coding: utf-8 -*-

class Translator:
  #приводит все буквы к заглавным кириллическим или заглавным латинским, чтобы поискать и так и так
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
        u'С': u'С',
        u'Т': u'T',
        u'У': u'Y',
        u'Х': u'X',
        u'а': u'A',
        u'в': u'B',
        u'е': u'E',
        u'к': u'K',
        u'м': u'M',
        u'н': u'H',
        u'о': u'O',
        u'р': u'P',
        u'с': u'C',
        u'т': u'T',
        u'у': u'Y',
        u'х': u'X'
      }
      match_letters_En2Ru = {
        u'a': u'А',
        u'b': u'В',
        u'e': u'Е',
        u'k': u'К',
        u'm': u'М',
        u'h': u'Н',
        u'o': u'О',
        u'p': u'Р',
        u'c': u'С',
        u't': u'Т',
        u'y': u'У',
        u'x': u'Х',
        u'A': u'А',
        u'B': u'В',
        u'E': u'Е',
        u'K': u'К',
        u'M': u'М',
        u'H': u'Н',
        u'O': u'О',
        u'P': u'Р',
        u'С': u'С',
        u'T': u'Т',
        u'Y': u'У',
        u'X': u'Х'
      }
      match_letters = match_letters_En2Ru
      if direction == 'Ru2En':
        match_letters = match_letters_Ru2En

      translit_string = u""
      string = string.replace(' ', '')

      for index, char in enumerate(string, 1):
        # print(char, index)
        if index in {2, 5, 7}:
          translit_string += ' '
        char = char.upper()
        repl = match_letters.get(char)
        if not repl:
          repl = char
        translit_string += repl

      return translit_string