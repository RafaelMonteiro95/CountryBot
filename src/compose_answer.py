##############################################
# Processamento de Linguagem Natural SCC0633 #
# Natural answer generation source file      #
#                                            #
# Giovanna Oliveira Guimarães   9293693      #
# Lucas Alexandre Soares        9293265      #
# Rafael Joegs Monteiro         9293095      #
# Darlan Xavier Nascimento      10867851     #
#                                            #
##############################################


import sys

# Replaces the question pronoun in order to 
# compose the answer
def _replace_pronoun(parsed, answer):
	phrase = parsed.question.replace("?", "")
	ans = phrase.split(" ")

	# x is a word of ans
	final = [answer if x == parsed.pron else x for x in ans]

	return " ".join(final)

# FIXME: placeholder answer generation
def compose_answer(parsed, answer):
	return _replace_pronoun(parsed, answer)