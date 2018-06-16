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
import re
import spacy

from ChatbotException import ChatbotException

# Countries list
# Default list
# COUNTRY_LIST = ["China", "Brasil", "Rússia", "Japão", "México", "Egito", "Itália", "Nova Zelândia", "Somália", "Estados unidos", "França", "Austrália", "Reino Unido", "Países constituintes", "Índia", "Indonésia", "Paquistão", "Nigéria", "Bangladesh", "Filipinas", "Vietnã", "Etiópia", "Alemanha", "Irão", "Turquia", "Tailândia", "África do Sul", "Myanmar", "Tanzânia", "Coreia do Sul", "Colômbia", "Espanha", "Quénia", "Argentina", "Ucrânia", "Argélia", "Polónia", "Sudão", "Iraque", "Canadá", "Uganda", "Marrocos", "Arábia Saudita", "Peru", "Uzbequistão", "Malásia", "Venezuela", "Nepal", "Gana", "Afeganistão", "Iémen", "Moçambique", "Coreia do Norte", "Angola", "Síria", "Camarões", "Costa do Marfim", "Madagáscar", "Sri Lanka", "Roménia", "Níger", "Burkina Faso", "Chile", "Mali", "Cazaquistão", "Malawi", "Guatemala", "Equador", "Zâmbia", "Camboja", "Chade", "Senegal", "Zimbabwe", "Sudão do Sul", "Bolívia", "Ruanda", "Bélgica", "Cuba", "Tunísia", "Haiti", "Grécia", "Guiné", "República Checa", "República Dominicana", "Portugal", "Benim", "Hungria", "Burundi", "Suécia", "Azerbaijão", "Bielorrússia", "Emirados Árabes Unidos", "Honduras", "Áustria", "Israel", "Tajiquistão", "Suíça", "Jordânia", "Papua-Nova Guiné", "Togo", "Hong Kong", "Bulgária", "Sérvia", "Paraguai", "Laos", "Serra Leoa", "El Salvador", "Líbia", "Nicarágua", "Quirguistão", "Dinamarca", "Singapura", "Eslováquia", "Eritreia", "República Centro-Africana", "Costa Rica", "Turquemenistão", "Territórios palestinos", "República da Irlanda", "República do Congo", "Libéria", "Oman", "Croácia", "Líbano", "Puntlândia", "Bósnia e Herzegovina", "Panamá", "Geórgia", "Mauritânia", "Moldávia", "Porto Rico", "Somalilândia", "Uruguai", "Kuwait", "Mongólia", "Arménia", "Lituânia", "Albânia", "Jamaica", "Namíbia", "Lesoto", "Catar", "Botswana", "Eslovénia", "Letónia", "Gâmbia", "Guiné-Bissau", "Kosovo", "Gabão", "Bahrein", "Trinidad e Tobago", "Estónia", "Maurícia", "Guiné Equatorial", "Timor-Leste", "Suazilândia", "Djibouti", "Fiji", "Chipre", "Comores", "Butão", "Guiana", "Macau", "Montenegro", "Ilhas Salomão", "Luxemburgo", "Suriname", "Cabo Verde", "Saara Ocidental", "Transnístria", "Malta", "Guadalupe", "Brunei", "Martinica", "Bahamas", "Belize", "Maldivas", "Islândia", "Barbados", "Nova Caledônia", "Polinésia Francesa", "Vanuatu", "Abecásia", "Guiana Francesa", "Mayotte", "Santa Lúcia", "Guam", "Curaçao", "Nagorno-Karabakh", "São Vicente e Granadinas", "Aruba", "Kiribati", "Ilhas Virgens Americanas", "Tonga", "Jersey", "Seychelles", "Antigua e Barbuda", "Ilha de Man", "Ceuta", "Melilla", "Andorra", "Domínica", "Guernsey", "Bermudas", "Ilhas Marshall", "Gronelândia", "Ilhas Cayman", "Marianas Setentrionais", "Ossétia do Sul", "Ilhas Faroe", "Sint Maarten", "Liechtenstein", "Mónaco", "Saint-Martin", "San Marino", "Gibraltar", "Ilhas Turks e Caicos", "Ilhas Åland", "Finlândia", "Ilhas Virgens Britânicas", "Palau", "Bonaire", "Ilhas Cook", "Anguilla", "Wallis e Futuna", "Tuvalu", "Nauru", "São Pedro e Miquelon", "Montserrat", "Sint Eustatius", "Ilhas Malvinas", "Svalbard e Jan Mayen", "Noruega", "Ilha Norfolk", "Ilha Christmas", "Saba", "Niue", "Tokelau", "Vaticano", "Ilha Wake", "Midway Atoll", "Ilhas Pitcairn"]
# Lower case list
# COUNTRY_LIST = ['china', 'brasil', 'rússia', 'japão', 'méxico', 'egito', 'itália', 'nova zelândia', 'somália', 'estados unidos', 'frança', 'austrália', 'reino unido', 'países constituintes', 'índia', 'indonésia', 'paquistão', 'nigéria', 'bangladesh', 'filipinas', 'vietnã', 'etiópia', 'alemanha', 'irão', 'turquia', 'tailândia', 'áfrica do sul', 'myanmar', 'tanzânia', 'coreia do sul', 'colômbia', 'espanha', 'quénia', 'argentina', 'ucrânia', 'argélia', 'polónia', 'sudão', 'iraque', 'canadá', 'uganda', 'marrocos', 'arábia saudita', 'peru', 'uzbequistão', 'malásia', 'venezuela', 'nepal', 'gana', 'afeganistão', 'iémen', 'moçambique', 'coreia do norte', 'angola', 'síria', 'camarões', 'costa do marfim', 'madagáscar', 'sri lanka', 'roménia', 'níger', 'burkina faso', 'chile', 'mali', 'cazaquistão', 'malawi', 'guatemala', 'equador', 'zâmbia', 'camboja', 'chade', 'senegal', 'zimbabwe', 'sudão do sul', 'bolívia', 'ruanda', 'bélgica', 'cuba', 'tunísia', 'haiti', 'grécia', 'guiné', 'república checa', 'república dominicana', 'portugal', 'benim', 'hungria', 'burundi', 'suécia', 'azerbaijão', 'bielorrússia', 'emirados árabes unidos', 'honduras', 'áustria', 'israel', 'tajiquistão', 'suíça', 'jordânia', 'papua-nova guiné', 'togo', 'hong kong', 'bulgária', 'sérvia', 'paraguai', 'laos', 'serra leoa', 'el salvador', 'líbia', 'nicarágua', 'quirguistão', 'dinamarca', 'singapura', 'eslováquia', 'eritreia', 'república centro-africana', 'costa rica', 'turquemenistão', 'territórios palestinos', 'república da irlanda', 'república do congo', 'libéria', 'oman', 'croácia', 'líbano', 'puntlândia', 'bósnia e herzegovina', 'panamá', 'geórgia', 'mauritânia', 'moldávia', 'porto rico', 'somalilândia', 'uruguai', 'kuwait', 'mongólia', 'arménia', 'lituânia', 'albânia', 'jamaica', 'namíbia', 'lesoto', 'catar', 'botswana', 'eslovénia', 'letónia', 'gâmbia', 'guiné-bissau', 'kosovo', 'gabão', 'bahrein', 'trinidad e tobago', 'estónia', 'maurícia', 'guiné equatorial', 'timor-leste', 'suazilândia', 'djibouti', 'fiji', 'chipre', 'comores', 'butão', 'guiana', 'macau', 'montenegro', 'ilhas salomão', 'luxemburgo', 'suriname', 'cabo verde', 'saara ocidental', 'transnístria', 'malta', 'guadalupe', 'brunei', 'martinica', 'bahamas', 'belize', 'maldivas', 'islândia', 'barbados', 'nova caledônia', 'polinésia francesa', 'vanuatu', 'abecásia', 'guiana francesa', 'mayotte', 'santa lúcia', 'guam', 'curaçao', 'nagorno-karabakh', 'são vicente e granadinas', 'aruba', 'kiribati', 'ilhas virgens americanas', 'tonga', 'jersey', 'seychelles', 'antigua e barbuda', 'ilha de man', 'ceuta', 'melilla', 'andorra', 'domínica', 'guernsey', 'bermudas', 'ilhas marshall', 'gronelândia', 'ilhas cayman', 'marianas setentrionais', 'ossétia do sul', 'ilhas faroe', 'sint maarten', 'liechtenstein', 'mónaco', 'saint-martin', 'san marino', 'gibraltar', 'ilhas turks e caicos', 'ilhas åland', 'finlândia', 'ilhas virgens britânicas', 'palau', 'bonaire', 'ilhas cook', 'anguilla', 'wallis e futuna', 'tuvalu', 'nauru', 'são pedro e miquelon', 'montserrat', 'sint eustatius', 'ilhas malvinas', 'svalbard e jan mayen', 'noruega', 'ilha norfolk', 'ilha christmas', 'saba', 'niue', 'tokelau', 'vaticano', 'ilha wake', 'midway atoll', 'ilhas pitcairn']
# No accents and all lowercase list
COUNTRY_LIST = ['china', 'brasil', 'russia', 'japao', 'mexico', 'egito', 'italia', 'nova zelandia', 'somalia', 'estados unidos', 'franca', 'australia', 'reino unido', 'paises constituintes', 'india', 'indonesia', 'paquistao', 'nigeria', 'bangladesh', 'filipinas', 'vietna', 'etiopia', 'alemanha', 'irao', 'turquia', 'tailandia', 'africa do sul', 'myanmar', 'tanzania', 'coreia do sul', 'colombia', 'espanha', 'quenia', 'argentina', 'ucrania', 'argelia', 'polonia', 'sudao', 'iraque', 'canada', 'uganda', 'marrocos', 'arabia saudita', 'peru', 'uzbequistao', 'malasia', 'venezuela', 'nepal', 'gana', 'afeganistao', 'iemen', 'mocambique', 'coreia do norte', 'angola', 'siria', 'camaroes', 'costa do marfim', 'madagascar', 'sri lanka', 'romenia', 'niger', 'burkina faso', 'chile', 'mali', 'cazaquistao', 'malawi', 'guatemala', 'equador', 'zambia', 'camboja', 'chade', 'senegal', 'zimbabwe', 'sudao do sul', 'bolivia', 'ruanda', 'belgica', 'cuba', 'tunisia', 'haiti', 'grecia', 'guine', 'checa', 'dominicana', 'portugal', 'benim', 'hungria', 'burundi', 'suecia', 'azerbaijao', 'bielorrussia', 'emirados arabes unidos', 'honduras', 'austria', 'israel', 'tajiquistao', 'suica', 'jordania', 'papua-nova guine', 'togo', 'hong kong', 'bulgaria', 'servia', 'paraguai', 'laos', 'serra leoa', 'el salvador', 'libia', 'nicaragua', 'quirguistao', 'dinamarca', 'singapura', 'eslovaquia', 'eritreia', 'centro-africana', 'costa rica', 'turquemenistao', 'territorios palestinos', 'irlanda', 'do congo', 'liberia', 'oman', 'croacia', 'libano', 'puntlandia', 'bosnia e herzegovina', 'panama', 'georgia', 'mauritania', 'moldavia', 'porto rico', 'somalilandia', 'uruguai', 'kuwait', 'mongolia', 'armenia', 'lituania', 'albania', 'jamaica', 'namibia', 'lesoto', 'catar', 'botswana', 'eslovenia', 'letonia', 'gambia', 'guine-bissau', 'kosovo', 'gabao', 'bahrein', 'trinidad e tobago', 'estonia', 'mauricia', 'guine equatorial', 'timor-leste', 'suazilandia', 'djibouti', 'fiji', 'chipre', 'comores', 'butao', 'guiana', 'macau', 'montenegro', 'ilhas salomao', 'luxemburgo', 'suriname', 'cabo verde', 'saara ocidental', 'transnistria', 'malta', 'guadalupe', 'brunei', 'martinica', 'bahamas', 'belize', 'maldivas', 'islandia', 'barbados', 'nova caledonia', 'polinesia francesa', 'vanuatu', 'abecasia', 'guiana francesa', 'mayotte', 'santa lucia', 'guam', 'curacao', 'nagorno-karabakh', 'sao vicente e granadinas', 'aruba', 'kiribati', 'ilhas virgens americanas', 'tonga', 'jersey', 'seychelles', 'antigua e barbuda', 'ilha de man', 'ceuta', 'melilla', 'andorra', 'dominica', 'guernsey', 'bermudas', 'ilhas marshall', 'gronelandia', 'ilhas cayman', 'marianas setentrionais', 'ossetia do sul', 'ilhas faroe', 'sint maarten', 'liechtenstein', 'monaco', 'saint-martin', 'san marino', 'gibraltar', 'ilhas turks e caicos', 'ilhas åland', 'finlandia', 'ilhas virgens britanicas', 'palau', 'bonaire', 'ilhas cook', 'anguilla', 'wallis e futuna', 'tuvalu', 'nauru', 'sao pedro e miquelon', 'montserrat', 'sint eustatius', 'ilhas malvinas', 'svalbard e jan mayen', 'noruega', 'ilha norfolk', 'ilha christmas', 'saba', 'niue', 'tokelau', 'vaticano', 'ilha wake', 'midway atoll', 'ilhas pitcairn']

# Lista de verbos de cópular (ligação)
VCOP_LIST = ["ser", "estar", "permanecer", "ficar", "tornar", "andar", "parecer", "virar", "continuar", "viver"]

# Pronoun list
PRONOUNS = ['quem', 'como', 'qual', 'quais', 'quando', 'quanto', 'quantos', 'quantas', 'onde', 'por que', 'por quê', 'que']
EXPECTED_ANSWER = {
	
	'quem': {
		'regra': ['PREP', 'PROPN'],
		'PREP': None,
		'INV_PREP': ['por', 'para'],
		'PROPN': {}
	},

	# TODO: usar Rule-Base Matching para identificar datas por exemplo 
	# 13/12/1996 ou 13.12.1996. Datas no formato 13 de dezembro de 1996 já é 
	# reconhecido como o padrão NUM de NOUM de NUM<year>
	'quando': 'data', 
	
	'quanto': 'numero',
	'quantos': 'numero',
	'quantas': 'numero',
	
	'onde': {
		'regra': ['PREP', 'PROPN'],
		'PREP': ['em', 'no', 'na'],
		'INV_PREP': None,
		'PROPN': {}
	},

	'por que': '',
	'por quê': '',
	'porque': '',
	'porquê': '',

	'que': '',
	'como': '',
	'qual': '',
	'quais': '',
}


# Load portuguese model
pt_model = spacy.load('pt')
# pergunta = input()
# pergunta = u"Quem é o presidente do Brasil?"
# doc = pt_model(pergunta)



class ParsedQuestion():

	def __init__(self, question, pron=None, country=None, topic=None):

		self.pergunta = question
		self.pergunta_canon = text_canonicalize(question)
		self.pron = pron
		self.pron_lower = pron.lower() if pron else None
		self.country = country
		self.topic = topic
		self.expected = EXPECTED_ANSWER[self.pron_lower] if pron else None

	def __repr__(self):
		s = "\n\nPergunta: {0}\n".format(self.pergunta)
		s += "Pronome: {0}\n".format(self.pron if self.pron else "none")
		s += "País: {0}\n".format(self.country if self.country else "none")
		s += "Topico: {0}\n".format(str(self.topic))
		s += "Tipo de resposta: {0}\n".format(str(self.expected))
		s += "Possível query: '{0}'".format(text_canonicalize(str(self.topic) + " " + str(self.country)))

		return s

	def __unicode__(self):
		return self.pergunta

	def __str__(self):
		return unicode(self).encode('utf-8')

	def __hash__(self):
		return self.pergunta.__hash__()

	def __eq__(self, other):
		return self.pergunta == other.pergunta



def _find_pron(doc):

	# Find all pronouns
	prons = [word for word in doc if word.pos_ == 'PRON']

	# Assume that the first pronoun is relative to our question
	for word in prons:
		# print("Checking word '{0}'".format(word.lower_))
		if word.lower_ in PRONOUNS:
			return word.text # Pronoun was found!
	
	# No pronoun found, maybe it was wrongly classified. Search in adverbs
	advs = [word for word in doc if word.pos_ == 'ADV']

	# Search for word in valid pronouns list
	for word in advs:
		if word.pos_ in PRONOUNS:
			return word.text # Pronoun was found!
	
	# Still no pronoun found, brute force it
	for word in doc:
		if word.lower_ in PRONOUNS:
			return word.text

	# If it still wasnt found, we dont have a valid pronoun
	if not pron:
		err_msg = "[Error] Nenhum pronome encontrado na pergunta."
		print(err_msg)
		raise ChatbotException(msg=err_msg, question=doc.text)

	# Not found
	return None


def _find_country(doc):

	# Search for Named Entities in doc
	for ent in doc.ents:
		tmp = text_canonicalize(ent.lower_)
		if not "republica" in tmp and tmp in COUNTRY_LIST:
			return tmp

	# No valid named entity, fallback
	# Find all proper nouns (country os person names)
	propns = [word for word in doc if word.pos_ == 'PROPN' and not word.text.isupper()]

	# Process country name
	try:
		# Assume that the first proper noun is our country name
		propn = propns[0].lower_
		
		# If our proper noun is not in country's list, its an invalid country
		if not propn in COUNTRY_LIST:
			
			for word in doc:
				if word.lower_ in COUNTRY_LIST:
					return word.text

	except IndexError as e:
		err_msg = "[Error] Nenhum país encontrado na pergunta."
		print(err_msg)
		raise ChatbotException(e, err_msg, doc.text)
	
	except Exception as e:
		err_msg = "[Error] País '{0}' desconhecido.".format(propn)
		print(err_msg)
		raise ChatbotException(e, err_msg, doc.text)

	# Not found
	return None

# These are used to compose TOPIC
def _find_nouns(doc):

	# Process nouns - try to find the question's topic
	nouns = [word for word in doc if word.pos_ == 'NOUN']
	return " ".join([word.lower_ for word in nouns])

def _find_adjs(doc):

	# Process adjectives - try to find the question's topic
	adjs = [word for word in doc if word.pos_ == 'ADJ']
	return " ".join([word.lower_ for word in adjs])

def _find_verbs(doc, exclude_cop=True):

	# Process verbs
	verbs = [word for word in doc if word.pos_ == 'VERB']
					
	# Filter out cop verbs if not explicity asked since they dont bring
	# information by themselves
	if exclude_cop:
		verbs = [word for word in verbs if not word.lemma_ in VCOP_LIST]

	return " ".join([word.lower_ for word in verbs])

def _find_abbreviations(doc):
	return [abbv.text for abbv in doc if abbv.text.isupper()]

def _find_leftovers(doc):

	# Process the rest of the tagset - try to find the question's topic
	left = [word for word in doc if word.pos_ == 'SYM']
	return " ".join([word.lower_ for word in left])

# Shorthand for calling each find and concatenating their results
def _find_topic(doc, exclude_cop=True):

	topic = _find_verbs(doc, exclude_cop=True) + " " + \
			_find_nouns(doc) + " " + \
			_find_leftovers(doc) + " " + \
			_find_adjs(doc) + " " + \
			" ".join(_find_abbreviations(doc))

	return topic.strip()

# To find places or people's names
def _find_proper_nouns(doc):
	pass

def parse_question(question, pron=None, country=None, model=pt_model):

	question = re.sub("[\n]", "", question)
	doc = model(question)

	if not pron: 
		try: pron = _find_pron(doc)
		except Exception as e: 
			print(e)
			pron = None

	if not country: 
		try: country = _find_country(doc)
		except: country = None
	
	abbrvs = _find_abbreviations(doc)
	topic = _find_topic(doc)

	return ParsedQuestion(question, pron, country, topic)


# Compiled regexes for canincalizing text
regex = [ re.compile("[áàâãäåÁÀÂÃÄÅ]"),
	re.compile("[éèêẽëÉÈÊẼË]"),
	re.compile("[íìîĩïÍÌÎĨÏ]"),
	re.compile("[óòôõöÓÒÔÕÖ]"),
	re.compile("[úùûũüÜÚÙÛŨ]"),
	re.compile("[ýỳŷỹÿÝỲŶỸŸ]"),
	re.compile("[çÇ]"),
	re.compile("[ñ]"),
	re.compile("\\s+"),
]
def text_canonicalize(question):

	question = re.sub(regex[0], "a", question)
	question = re.sub(regex[1], "e", question)
	question = re.sub(regex[2], "i", question)
	question = re.sub(regex[3], "o", question)
	question = re.sub(regex[4], "u", question)
	question = re.sub(regex[5], "y", question)
	question = re.sub(regex[6], "c", question)
	question = re.sub(regex[7], "n", question)
	question = re.sub(regex[8], " ", question)
	return question


def test(path="../perguntas.txt", debug=False):

	file = open(path)
	lines = file.readlines()
	lines = [line.rstrip() for line in lines if line[0] != '#']

	res = []

	counter = 0
	for line in lines:
		try:
			if debug: print(line)
			res.append(parse_question(line))

		except ChatbotException as e:
			res.append({
				"err_msg": "Erro na pergunta '{0}'".format(line), 
				"exception": e,
				"index": counter
			})

		except Exception as e:
			print("Unknown error occured. Error msg: '{0}'.".format(repr(e)))
			# raise e

		finally:
			counter += 1

	return res

def _get_lists(res):

	no_pron = [r for r in res if not r.pron]
	no_country = [r for r in res if not r.country]
	return {'no_pron': no_pron, 'no_country': no_country}