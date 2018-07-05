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

### Question answering imports
import random
from parse_question import parse_question
from get_answer import get_answer
from compose_answer import compose_answer
from ChatbotException import ChatbotException

username = None;

def main():
	#variables used for storing parsed questions
	parsed = None
	last_parsed = None

	print('Essa é uma demonstração das funcionalidades do chatbot.')
	print('Este programa não utiliza um banco de dados, então seu nome e sua última pergunta não serão salvos após a finalização da execução.')
	print('Como o programa monta um cache baixando as páginas de cada país, a primeira pergunta sobre um país pode demorar um pouco.')
	print('Chatbot: Olá, qual é o seu nome?')
	username = input('Usuário: ').strip()
	print('Chatbot: Olá {0}!'.format(username))
	

	while True:
		try:
			# Variable to check if i'm using the last question
			print("Chatbot: me pergunte algo sobre um país!")
			user_question = input('Usuário: ').strip()
			parsed = parse_question(user_question)
			first_parsed = parse_question(user_question)

			#parsing answer for topic and country
			try:
				res = get_answer(parsed)
			except ChatbotException as e:
				#This exception occurs when the parsing does not finds the country
				res = 'Country not Found'
			first_info = res

			#checking if parsing went wrong
			if res == 'Country not Found':
				#try using last question country
				if last_parsed:
					parsed.country = last_parsed.country
					try:
						res = get_answer(parsed)
					except:
						res = None
					if res == 'Topic not Found':
						res = None
				else:
					res = None

			elif res == 'Topic not Found':
				#try using last question Topic
				if last_parsed:
					parsed.topic = last_parsed.topic
					try:
						res = get_answer(parsed)
					except ChatbotException as e:
						res = None
				else:
					res = None

			print('===RESPOSTA===')
			if res:
				answer = compose_answer(parsed, res)
				print('Chatbot: ',answer)
				last_parsed = parsed
			else:
				print('Chatbot: Não consegui encontrar uma resposta.')

			print('===\nO que foi extraído dessa pergunta:')
			print(first_parsed,'\n')
			print('Informação que foi encontrada na base de dados:')
			print(first_info,'\n', '===', end='\n\n\n')
		except KeyboardInterrupt:
			print('Saindo...')
			exit(0)


if __name__ == '__main__':
	main()