import sys

class ChatbotException(Exception):

	def __init__(self, e, msg=None, question=None, pron=None, country=None):
		
		self.e = e
		self.msg = msg
		self.question = question
		self.pron = pron
		self.country = country

	def __repr__(self):
		s = "%s in question '%s'.\n" % self.msg, self.question
		return s + str(self.e)
