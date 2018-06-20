import telebot
import time
from tinydb import TinyDB, Query, where
from threading import Thread

#Creating a bot instance
#This needs to be global so all message handlers can have access to the bot
db = TinyDB('db.json')
bot = telebot.TeleBot("534643979:AAFWymR8hBdtXZKiNzem7EcyiZxy_V5fWUM");
users = []


#this handler will execute once a user send a message to the bot with the command start i.e. "/start"
@bot.message_handler(commands=['start'])
def start_handler(message):
	users.append(message.chat.id)
	bot.send_message(message.chat.id, "Olá! Qual é o seu nome?")
	db.insert({'id': message.chat.id, 'name': 'unnamed user', 'state': 'waiting_for_name'})


#this handler will execute once a user not in users list sends a message to the bot
@bot.message_handler(func=lambda message: message.chat.id not in users)
def unknown_user_handler(message):
	bot.send_message(message.chat.id, "Olá! Acho que ainda não te conheço. Envie /start para começarmos a conversar")


#this handler will execute once a user in users list sends a message to the bot
@bot.message_handler(func=lambda message: message.chat.id in users)
def known_user_handler(message):
	#fetch user in database
	user = db.get(where('id') == message.chat.id)

	#checks for user state and answer accordingly
	#if bot is waiting for user to say its name
	if user['state'] == 'waiting_for_name':
		#update and insert user name and state
		db.upsert({'name': message.text, 'state': 'waiting_for_question'}, where('id') == user['id'])
		#generates an answer string by fetching the user name from the database
		answer = "Olá {0}, me pergunte algo sobre um país!".format( db.get(where('id') == user['id'])['name'] )
		#sends answer as a message to user 
		bot.send_message(user['id'], answer)
	#if bot is waiting for user to ask a question
	elif user['state'] == 'waiting_for_question':
		#sample code; Insert something useful here
		bot.send_message(user['id'], 'Eco: ' + message.text)


def main():

	#loading users in database
	#cleans the database
	# db.purge()
	print('Loading users...')
	#loads all users id's in database to the 'users' list
	users = [result['id'] for result in db.all()]
	print(len(users), 'users in database')
	print('users:',[result['name'] for result in db.all()])

	#starting bot thread
	#thread is in daemon mode so when the script ends the threads are terminated
	#thread executes the bot.polling() function which fetchs for messages
	thread = Thread(target=bot.polling,args=())
	thread.daemon = True
	thread.start();

	#now main is free to do whatever it likes
	while True:
		try:
			time.sleep(1)
			#here we can print stuff
		except KeyboardInterrupt:
			print("Stopping server...")
			exit(0)


if __name__ == '__main__':
	main()