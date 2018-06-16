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
# from XXX import XXX -- NOTE: this is for getting answer for external source - DEPS: Joegs
from ChatbotException import ChatbotException

### Lists with multiple answers for more organic chat
GREETINGS = ["Olá! Sou um Chatbot sobre países do mundo, qual é o seu nome?\n"]
FAREWELLS = ["Foi bom conversar com você, até mais!\n"]
UNKNOWN_QUESTION_ANSWERS = ["Desculpe, não entendi sua pergunta.\n"]
UNKNOWN_COUNTRY_ANSWERS = ["Desculpe, não reconheço este país\n"]
ASK_AGAIN = ["Você pode tentar me dizer outro país ou pedir para refazer a pergunta.\n"]
CONFIRM_COUNTRY = ["Você ainda está falando do país {0}?\n"]
CONFIRM_TOPIC = ["Você ainda está falando sobre {0}?\n"]

# NOTE: chatbot should be a class or simply a method?
def StartChatbot():
	
	name = input(random.choice(GREETINGS))
	chatting = True
	print("Bom dia {0}, pode começar a perguntar!\n".format(name))
	
	topic_mem = ''
	country_mem = ''

	# Keep talking
	while(chatting):
		
		abort_question = False

		# Ask question
		question = input()
		parsed = parse_question(question)

		# If no pronoun was found, we cant interpret the question, so asked user
		# to rewrite the question
		if not parsed.pron:
			print(random.choice(UNKNOWN_QUESTION_ANSWERS))
			continue
			

		# Keep asking for country name until a recognizable one is given or user
		# ask another question
		while not parsed.country and not abort_question:
			
			print(random.choice(UNKNOWN_COUNTRY_ANSWERS))
			print(random.choice(ASK_AGAIN))
			
			country = input()
			_country = country.lower()
			
			if _country in COUNTRY_LIST: parsed.country = country
			elif 	("outra" in _country and "pergunta" in _country or)
					("mudar" in _country and "pergunta" in _country or)
					("trocar" in _country and "pergunta" in _country or)
					("refazer" in _country and "pergunta" in _country):
					abort_question = True

		#Topic and country memory will be used for more fluid and realistic chat
		topic_mem = parsed.topic
		country_mem = parsed.country

		print("[Debug]: Parsed question:\n")
		print(parsed)
		print()
		print("Próxima pergunta!")

	print(random.choice(FAREWELLS))


if __name__ == "__main__":
	StartChatbot()
