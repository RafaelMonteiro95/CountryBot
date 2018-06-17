##############################################
# Processamento de Linguagem Natural SCC0633 #
# General countries Chatbot main source file #
#                                            #
# Giovanna Oliveira Guimarães   9293693      #
# Lucas Alexandre Soares        9293265      #
# Rafael Joegs Monteiro         9293095      #
# Darlan Xavier Nascimento      10867851     #
#                                            #
##############################################
	
import random

from parse_question import parse_question, text_canonicalize
from parse_question import COUNTRY_LIST
from compose_answer import compose_answer
from get_answer import get_answer
from ChatbotException import ChatbotException

### Lists with multiple answers for more organic chat
GREETINGS = ["Olá! Sou um Chatbot sobre países do mundo, qual é o seu nome?\n"]
FAREWELLS = ["Foi bom conversar com você, até mais!\n"]
UNKNOWN_QUESTION_ANSWERS = ["Desculpe, não entendi sua pergunta.\n"]
UNKNOWN_COUNTRY_ANSWERS = ["Desculpe, não reconheço este país\n"]
ASK_AGAIN = ["Você pode tentar me dizer outro país ou pedir para refazer a pergunta.\n"]
CONFIRM_COUNTRY = ["Você ainda está falando do país {0}?\n"]
CONFIRM_TOPIC = ["Você ainda está falando sobre {0}?\n"]
NO_ANSWER = ["Desculpa, não sei responder a sua pergunta.\n"]


index_mundi_base_url = "https://indexmundi.com/pt/"

def StartChatbot():
	
	name = input(random.choice(GREETINGS))
	chatting = True
	topic_mem = ''
	country_mem = ''

	question_msg = "Bom dia, {0}, pode começar a perguntar!\n".format(name)

	# Keep talking
	while(chatting):
		
		abort_question = False

		# Ask question
		print(question_msg)
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
			
			if _country in COUNTRY_LIST: parsed.country = _country
			elif 	("outra" in _country and "pergunta" in _country) or 	\
					("mudar" in _country and "pergunta" in _country) or 	\
					("trocar" in _country and "pergunta" in _country) or 	\
					("refazer" in _country and "pergunta" in _country):
					abort_question = True

		if _country == 'usa' or _country == 'eua':
			parse_question.country = 'estados unidos'

		# Go to next iteration to ask for next question
		if abort_question: 
			question_msg = "Ok, vamos mudar a pergunta." # probably temporary
			continue
		
		print("[Debug]: Parsed question:\n")
		print(parsed)
		print()
		question_msg = "Próxima pergunta!" # probably temporary

		#Topic and country memory will be used for more fluid and realistic chat
		topic_mem = parsed.topic
		country_mem = parsed.country

		# Question was successfuly parsed, try to find the answer
		# answer = find_answer()
		answer = None

		if answer:
			# print(compose_answer(question, answer))
			pass
		else:
			print("Ainda não implementado")
			# print(random.choice(NO_ANSWER))

	# Say goodbye!
	print(random.choice(FAREWELLS))
	return


if __name__ == "__main__":
	StartChatbot()



# Debug
def test(question):
	res = pq(question)
	ans = get_answer(res)
	return Ans(res, ans)

