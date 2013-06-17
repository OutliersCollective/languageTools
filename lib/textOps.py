__author__ = 'oscarmarinmiro'
# -*- coding: utf8 -*-

import re


def removeRubbish(text):
    text = text.encode('utf-8')
    # Quito las url's
    text = re.sub(r'http\:\/\/([^ ])*', "", text)
    # Quito los numeros

    #text = re.sub(r'(\d)+'," ",text)

    #coma de abrir y cerrar
    text = text.replace('“',' ')
    text = text.replace('”',' ')
    text = text.replace('’',' ')
    text = text.replace('&',' ')
    text = text.replace('"' , ' ')
    text = text.replace('(' , ' ')
    text = text.replace(')' , ' ')
    text = text.replace('!' , ' ')
    text = text.replace('¡' , ' ')
    text = text.replace('?' , ' ')
    text = text.replace('¿' , ' ')
    text = text.replace(',' , ' ')
    text = text.replace(';' , ' ')
    text = text.replace(':' , ' ')
    text = text.replace('.' , ' ')
    text = text.replace('...' , ' ')
    text = text.replace('+' , ' ')
    text = text.replace('%' , ' ')
    text = text.replace('-' , ' ')
    text = text.replace('{' , ' ')
    text = text.replace('}' , ' ')
    text = text.replace('[' , ' ')
    text = text.replace(']' , ' ')
    text = text.replace('*' , ' ')
    text = text.replace('^' , ' ')

    text = text.decode("utf-8")

    return text

def flattenCatsHash(text):
    text = text.encode('utf-8')
    text = text.lower()
    text = text.replace('á' , 'a')
    text = text.replace('é' , 'e')
    text = text.replace('í' , 'i')
    text = text.replace('ó' , 'o')
    text = text.replace('ú' , 'u')
    text = text.replace('à' , 'a')
    text = text.replace('è' , 'e')
    text = text.replace('ì' , 'i')
    text = text.replace('ò' , 'o')
    text = text.replace('ù' , 'u')
    text = text.replace('ü' , 'u')
    text = text.replace('ï' , 'i')
    text = text.replace('l·l' , 'll')
    text = text.replace('l•l' , 'll')
    text = text.replace('l.l' , 'll')
    text = text.replace('\t' , '')
    text = text.replace('\n' , '')
    text = text.replace("\\" , '')
    text = text.replace('á' , 'a')
    text = text.replace('é' , 'e')
    text = text.replace('í' , 'i')
    text = text.replace('ó' , 'o')
    text = text.replace('ú' , 'u')
    text = text.replace('"' , ' ')
    text = text.replace('(' , ' ')
    text = text.replace(')' , ' ')
    text = text.replace('!' , ' ')
    text = text.replace('¡' , ' ')
    text = text.replace('?' , ' ')
    text = text.replace('¿' , ' ')
    text = text.replace(',' , ' ')
    text = text.replace(';' , ' ')
    text = text.replace(':' , ' ')
    text = text.replace('.' , ' ')
    text = text.replace('#','')

    text = text.decode('utf-8')

    return text

def flattenCats(text):
    text = text.encode('utf-8')
    text = text.lower()
    text = text.replace('á' , 'a')
    text = text.replace('é' , 'e')
    text = text.replace('í' , 'i')
    text = text.replace('ó' , 'o')
    text = text.replace('ú' , 'u')
    text = text.replace('à' , 'a')
    text = text.replace('è' , 'e')
    text = text.replace('ì' , 'i')
    text = text.replace('ò' , 'o')
    text = text.replace('ù' , 'u')
    text = text.replace('ü' , 'u')
    text = text.replace('ï' , 'i')
    text = text.replace('l·l' , 'll')
    text = text.replace('l•l' , 'll')
    text = text.replace('l.l' , 'll')
    text = text.replace('\t' , '')
    text = text.replace('\n' , '')
    text = text.replace("\\" , '')
    text = text.replace('á' , 'a')
    text = text.replace('é' , 'e')
    text = text.replace('í' , 'i')
    text = text.replace('ó' , 'o')
    text = text.replace('ú' , 'u')
    text = text.replace('"' , ' ')
    text = text.replace('(' , ' ')
    text = text.replace(')' , ' ')
    text = text.replace('!' , ' ')
    text = text.replace('¡' , ' ')
    text = text.replace('?' , ' ')
    text = text.replace('¿' , ' ')
    text = text.replace(',' , ' ')
    text = text.replace(';' , ' ')
    text = text.replace(':' , ' ')
    text = text.replace('.' , ' ')

    text = text.decode('utf-8')

    return text

def okNameWikipedia(text):

    # Si tiene : o es solo numeros, me lo peino

    if re.search(r'\:',text) is not None:
        return False

    if re.search(r'^\d+$',text) is not None:
        return False


    return True

def cleanWikipedia(text):

    # Me peino los parentesis, los ' escapados y los _

    text = text.encode('utf-8')
    text = re.sub(r'\(.*?\)' , '',text)
    text = text.replace("\\'" , "'")
    text = text.replace("_" , " ")
    text = text.rstrip(" ")
    text = text.decode('utf-8')
    return text

def cleanWikilink(text):

    # Me peino los ' escapados y los _

    text = text.encode('utf-8')
#    text = re.sub(r'\(.*?\)' , '',text)
    text = text.replace("\\'" , "'")
    text = text.replace("_" , " ")
    text = text.decode('utf-8')
    return text


def flattenWikipedia(text):
    text = text.encode('utf-8')
    text = text.lower()
    text = text.replace('á' , 'a')
    text = text.replace('é' , 'e')
    text = text.replace('í' , 'i')
    text = text.replace('ó' , 'o')
    text = text.replace('ú' , 'u')
    text = text.replace('à' , 'a')
    text = text.replace('è' , 'e')
    text = text.replace('ì' , 'i')
    text = text.replace('ò' , 'o')
    text = text.replace('ù' , 'u')
    text = text.replace('ü' , 'u')
    text = text.replace('ï' , 'i')
    text = text.replace('l·l' , 'll')
    text = text.replace('l•l' , 'll')
    text = text.replace('l.l' , 'll')
    text = text.replace('\t' , '')
    text = text.replace('\n' , '')
    text = text.replace('á' , 'a')
    text = text.replace('é' , 'e')
    text = text.replace('í' , 'i')
    text = text.replace('ó' , 'o')
    text = text.replace('ú' , 'u')
    text = text.replace('"' , ' ')
    text = text.replace('(' , ' ')
    text = text.replace(')' , ' ')
    text = text.replace('!' , ' ')
    text = text.replace('¡' , ' ')
    text = text.replace('?' , ' ')
    text = text.replace('¿' , ' ')
    text = text.replace(',' , ' ')
    text = text.replace(';' , ' ')
    text = text.replace(':' , ' ')
    text = text.replace('.' , ' ')
    text = text.decode('utf-8')
    return text


def flattenNERInputEs(text):
    text = text.encode('utf-8')
    text = text.lower()
    text = text.replace('á' , 'a')
    text = text.replace('é' , 'e')
    text = text.replace('í' , 'i')
    text = text.replace('ó' , 'o')
    text = text.replace('ú' , 'u')
    text = text.replace('à' , 'a')
    text = text.replace('è' , 'e')
    text = text.replace('ì' , 'i')
    text = text.replace('ò' , 'o')
    text = text.replace('ù' , 'u')
    text = text.replace('ü' , 'u')
    text = text.replace('ï' , 'i')
    text = text.replace('\t' , ' ')
    text = text.replace('\n' , ' ')
    text = text.replace('\r' , ' ')
    text = text.replace('á' , 'a')
    text = text.replace('é' , 'e')
    text = text.replace('í' , 'i')
    text = text.replace('ó' , 'o')
    text = text.replace('ú' , 'u')
    text = text.decode('utf-8')
    return text
