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

import sys
import parse_question

class ChatbotException(Exception):

	def __init__(self, e=None, msg=None, question=None, pron=None, country=None):
		
		self.e = e
		self.msg = msg
		self.question = question
		self.canon_question = parse_question.text_canonicalize(question)
		self.pron = pron
		self.country = country

	def __repr__(self):
		s = "{0} in question '{1}'.\n".format(self.msg, self.question)
		return s + repr(self.e)


	# TODO: check unicode override
	def __unicode__(self):
		return self.__repr__()

	def __str__(self):
		return self.__repr__()
		# TODO: check unicode function
		# return unicode(self).encode('utf-8')
