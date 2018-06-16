import sys
from parse_question import text_canonicalize

class ChatbotException(Exception):

	def __init__(self, e=None, msg=None, question=None, pron=None, country=None):
		
		self.e = e
		self.msg = msg
		self.question = question
		self.canon_question = text_canonicalize(question)
		self.pron = pron
		self.country = country

	def __repr__(self):
		s = "{0} in question '{1}'.\n".format(self.msg, self.question)
		return s + repr(self.e)


	def __unicode__(self):
		return self.__repr__()

	def __str__(self):
		return unicode(self).encode('utf-8')
