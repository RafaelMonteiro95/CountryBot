##############################################
# Processamento de Linguagem Natural         #
# SCC0633                                    #
# General countries Chatbot main source file #
#                                            #
# Giovanna Oliveira Guimarães   9293693      #
# Lucas Alexandre Soares        9293265      #
# Rafael Joegs Monteiro         9293095      #
# Darlan Xavier                 XXX          #
#                                            #
##############################################

import random

from parse_question import parse_question, text_canonicalize
from parse_question import COUNTRY_LIST
# from compose_answer import XXX
from ChatbotException import ChatbotException

UNKNOWN_QUESTION_ANSWERS = ["Desculpe, não entendi sua pergunta"]

# NOTE: chatbot should be a class or simply a method?
def Chatbot():
	
	name = input("Olá! Sou um Chatbot sobre países do mundo, qual é o seu nome?")
	chatting = True
	print("Bom dia {0}, pode começar a perguntar!\n".format(name))
	
	while(chatting):
		
		question = input()
		parsed = parse_question(question)

		if not parsed.pron:
			print(random.choice(UNKNOWN_QUESTION_ANSWERS))

		while not parsed.country:
			country = input("Desculpe, não conheço este país, você poderia me dizer outro país?\n")
			if country.lower() in COUNTRY_LIST: parsed.country = country
			else: pass


