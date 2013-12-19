#!/usr/bin/python
# -*- coding: UTF-8 -*-


from urllib2 import urlopen
from urllib import urlencode

def blank_string(string, value=0):                  #This function checks if the input is empty.
    if len(string) == 0: return True  #It's empty
    for i in range(len(string)):
        if string[i] == ' ':
            value +=1
    if value == len(string): return True   #It's empty

def decorator(f):
    def inner(*args, **kwargs):
        #we check if the string is blank
        if blank_string(args[0]):
            return ''
        try:
            result = f(*args, **kwargs)
        except:
            return 'Check your internet connection'
        return result
    return inner


@decorator
def translate(text, lang1, lang2):      #Main function that takes care of the translation.

    langpair='%s|%s'%(lang1,lang2)      #Define a translation tuple with both languages.
    base_url='http://ajax.googleapis.com/ajax/services/language/translate?'
    params=urlencode( (('v',1.0),       #Encode all the parameters.
                      ('q',text),
                      ('langpair',langpair),) )
    url=base_url+params
    content=urlopen(url).read()         #Send the request and read the response.

    if "translatedText" not in content:
        return 'Something is Wrong with the Google Translate API'
#   usual response = {"responseData": {"translatedText":"Hello world"}, "responseDetails": null, "responseStatus": 200}
    start_idx = content.find('"translatedText":"')+18       #Search for the translated text inside the response.

                    #Response processing.
    translation = content[start_idx:]
    end_idx = translation.find('"}, "')
    translation = translation[:end_idx]
    translation_done = translation.replace("""\u0026quot;""", """'""")
                    #Response processing.

    print text.upper() + ' from ' + lang1.upper() + ' to ' + lang2.upper() + ' is ' + translation_done.upper()      #Log.

    if text == translation_done:
        return 'There is no translation for that'      #Checks if google translator could actually translate.
    else:
        return translation_done       #Returns the translation.
