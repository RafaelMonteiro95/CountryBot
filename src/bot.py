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

### Telegram Bot imports
import telebot
import time
from tinydb import TinyDB, where
from threading import Thread

### File managing, etc imports
import os

#Creating a bot instance
#This needs to be global so all message handlers can have access to the bot
db = TinyDB('db.json')
bot = telebot.TeleBot("534643979:AAFWymR8hBdtXZKiNzem7EcyiZxy_V5fWUM");


#this handler will execute once a user send a message to the bot with the command start i.e. "/start"
@bot.message_handler(commands=['start'])
def start_handler(message):
	#if the user is already in the database:
	if db.contains(where('id') == message.chat.id):
		bot.send_message(message.chat.id, "Eu já te conheço! Se quiser ser esquecido, use o comando /forget")
	else:
		bot.send_message(message.chat.id, "Olá! Qual é o seu nome?")
		db.insert({'id': message.chat.id, 'name': 'unnamed user', 'state': 'waiting_for_name'})


#this handler will execute once a user send a message to the bot with the command forget i.e. "/forget"
@bot.message_handler(commands=['forget'])
def remove_handler(message):
	db.remove(where('id') == message.chat.id)
	bot.send_message(message.chat.id, "Ok, te esqueci")


#this handler will execute once a user send a message to the bot with the command forget i.e. "/ping"
@bot.message_handler(commands=['ping'])
@bot.message_handler(func=lambda m: m.text.strip().lower() == 'ping')
def remove_handler(message):
	bot.send_message(message.chat.id, "pong")
	bot.send_video(message.chat.id, "https://i.imgur.com/ygVyp9N.gif")


#this handler will execute once a user not in users list sends a message to the bot
@bot.message_handler(func=lambda message: not db.contains(where('id') == message.chat.id))
def unknown_user_handler(message):
	bot.send_message(message.chat.id, "Olá! Acho que ainda não te conheço. Envie /start para começarmos a conversar")


#this handler will execute once a user in users list sends a message to the bot
@bot.message_handler(func=lambda message: db.contains(where('id') == message.chat.id))
def known_user_handler(message):
	#fetch user in database
	user = db.get(where('id') == message.chat.id)

	#checks for user state and answer accordingly
	#if bot was waiting for user to say its name
	if user['state'] == 'waiting_for_name':
		#update and insert user name and state
		db.upsert({'name': message.text, 'state': 'waiting_for_question'}, where('id') == user['id'])
		#generates an answer string by fetching the user name from the database
		answer = "Olá {0}, me pergunte algo sobre um país!".format( db.get(where('id') == user['id'])['name'] )
		#sends answer as a message to user 
		bot.send_message(user['id'], answer)


	#if bot was waiting for user to ask a question
	elif user['state'] == 'waiting_for_question':
		using_last_question = False

		#opening a file to store the conversation
		conv = open('conversations/{0}.txt'.format(user['id']), 'a', encoding = 'utf-8')
		#parsing user question
		parsed = parse_question(message.text.strip())
		#saving parsed question
		print(parsed, file=conv)

		#searching for an answer based on parsed question
		try:
			res = get_answer(parsed)
		except ChatbotException as e:
			#This exception occurs when the parsing does not finds the country
			res = 'Country not Found'
		except Exception as e:
			#If anything weird happens, this exception is handled
			print('bot: Unknown exception found when parsing answer')
			#saving the exception code to a log .txt file
			with open('logs/{0}.txt'.format(user['id']), encoding='utf-8') as log:
				print(e,file=log) 
			res = None

		#processing answer found
		if res == 'Country not Found':
			print('bot: Country not Found for user {0}'.format(user['name']))
			print('Country not found',file=conv)
			#Topic not found, search for user last question
			#Try-Catch block because user might not have a last question assigned
			try:
				last_parsed = user['last_question']
				using_last_question = True
				#Assigns last question topic to this question
				print('Using previous question country:',last_parsed['country'], file=conv)
				parsed.country = last_parsed['country']
				#try parsing again
				try:
					res = get_answer(parsed)
				except Exception as e:
					print('bot: Unknown exception found when parsing previous answer when country was not found')
					#saving the exception code to a log .txt file
					with open('logs/{0}.txt'.format(user['id']), encoding='utf-8') as log:
						print(e,file=log) 
					res = None
				if res == 'Topic not Found':
					print('Topic not found, this question cannot be answered (no topic, no country)', file=conv)
					#No topic: cannot answer this question
					res = None
			except KeyError:
				print('User has no previous question.',last_parsed['country'], file=conv)
				res = None

		elif res == 'Topic not Found':
			print('bot: Topic not Found for user {0}'.format(user['name']))
			print('Topic not found',file=conv)
			#Topic not found, search for user last question
			#Try-Catch block because user might not have a last question assigned
			try:
				last_parsed = user['last_question']
				using_last_question = True
				#Assigns last question topic to this question
				print('Using previous question topic:',last_parsed['topic'], file=conv)
				parsed.topic = last_parsed['topic']
				#try parsing again
				try:
					res = get_answer(parsed)
				except ChatbotException as e:
					#No country: cannot answer this question
					print('Country not found, this question cannot be answered (no topic, no country)', file=conv)
					res = None
				except Exception as e:
					print('bot: Unknown exception found when parsing previous answer when topic was not found')
					#saving the exception code to a log .txt file
					with open('logs/{0}.txt'.format(user['id']), encoding='utf-8') as log:
						print(e,file=log) 
					res = None
			except KeyError:
				print('User has no previous question.',last_parsed['country'], file=conv)
				res = None

		if res:
			#generating answer for user question
			answer = compose_answer(parsed, res)
			print('Answer:', answer, end='\n\n', file=conv)
			#saving this question for future uses
			db.update({'last_question': parsed}, where('id') == user['id'])
		else:
			print('Could not answer question', end='\n\n', file=conv)
			answer = 'Não consegui encontrar uma resposta.'

		#Sending answer to user
		bot.send_message(user['id'], answer)

def botPolling():
	while(True):
		try:
			bot.polling()
		except Exception as e:
			print(e)
			time.sleep(15)


def main():
	print('creating conversations folder')
	os.makedirs('conversations', exist_ok=True)
	os.makedirs('logs', exist_ok=True)

	#starting bot thread
	#thread is in daemon mode so when the script ends the thread is terminated
	#thread executes the bot.polling() function which fetchs for messages
	thread = Thread(target=botPolling,args=())
	thread.daemon = True
	thread.start();

	#now main is free to do whatever it likes
	prevUsers = None
	while True:
		try:
			time.sleep(1)
			users = [result['name']+'['+str(result['id'])+']' for result in db.all()]
			if users != prevUsers:
				print('bot: Current Users:')
				print(users)
				prevUsers = users
			#here we can print stuff
		except KeyboardInterrupt:
			print('bot: Stopping server...')
			exit(0)


if __name__ == '__main__':
	main()
