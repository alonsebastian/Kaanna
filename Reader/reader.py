#!/usr/bin/python
# -*- coding: UTF-8 -*-
from urllib2 import urlopen
from urllib import urlencode


def translate_text(archive_name, lang1, lang2):

    f = open (archive_name, "r")
    text = f.read()
    original_sentences = text.split (".")
    translated_sentences = []
    for original_sentence in original_sentences:
        translated_sentences.append (translate (original_sentence, lang1, lang2))

    output = open ("output.txt", "w")

    for sentence_number, original_sentence in enumerate(original_sentences):
        for index, letter in enumerate (original_sentence):
            if letter == '\n':
                number = 0
                try:
                    while True: #we look for a ' '
                        if translated_sentences[sentence_number][index + number] == ' ':
                            print index+number
                            translated_sentences[sentence_number] = translated_sentences[sentence_number][:index+number] + '\n' + translated_sentences[sentence_number][index+number:]
                            print "printed '/n' thing"
                            break
                        number -= 1
                        print number
                except IndexError: #there was nowhere to put the \n
                    pass

    #lines = []
    #for i in range (len(translated_sentences)):
    #    output.write (translated_sentences[i].split ("\n"))
    #for line in translated_sentences[i].split ("\n"):
    #    output.write(line)

    for i in range (len(translated_sentences)):
        for line in translated_sentences[i].split ("\n"):
            output.write(line+'\n')


        





if __name__ == "__main__":
    translate_text("datos.txt")


















