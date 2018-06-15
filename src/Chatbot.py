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
COUNTRY_LIST = ['china', 'brasil', 'russia', 'japao', 'mexico', 'egito', 'italia', 'nova zelandia', 'somalia', 'estados unidos', 'franca', 'australia', 'reino unido', 'paises constituintes', 'india', 'indonesia', 'paquistao', 'nigeria', 'bangladesh', 'filipinas', 'vietna', 'etiopia', 'alemanha', 'irao', 'turquia', 'tailandia', 'africa do sul', 'myanmar', 'tanzania', 'coreia do sul', 'colombia', 'espanha', 'quenia', 'argentina', 'ucrania', 'argelia', 'polonia', 'sudao', 'iraque', 'canada', 'uganda', 'marrocos', 'arabia saudita', 'peru', 'uzbequistao', 'malasia', 'venezuela', 'nepal', 'gana', 'afeganistao', 'iemen', 'mocambique', 'coreia do norte', 'angola', 'siria', 'camaroes', 'costa do marfim', 'madagascar', 'sri lanka', 'romenia', 'niger', 'burkina faso', 'chile', 'mali', 'cazaquistao', 'malawi', 'guatemala', 'equador', 'zambia', 'camboja', 'chade', 'senegal', 'zimbabwe', 'sudao do sul', 'bolivia', 'ruanda', 'belgica', 'cuba', 'tunisia', 'haiti', 'grecia', 'guine', 'checa', 'dominicana', 'portugal', 'benim', 'hungria', 'burundi', 'suecia', 'azerbaijao', 'bielorrussia', 'emirados arabes unidos', 'honduras', 'austria', 'israel', 'tajiquistao', 'suica', 'jordania', 'papua-nova guine', 'togo', 'hong kong', 'bulgaria', 'servia', 'paraguai', 'laos', 'serra leoa', 'el salvador', 'libia', 'nicaragua', 'quirguistao', 'dinamarca', 'singapura', 'eslovaquia', 'eritreia', 'centro-africana', 'costa rica', 'turquemenistao', 'territorios palestinos', 'da irlanda', 'do congo', 'liberia', 'oman', 'croacia', 'libano', 'puntlandia', 'bosnia e herzegovina', 'panama', 'georgia', 'mauritania', 'moldavia', 'porto rico', 'somalilandia', 'uruguai', 'kuwait', 'mongolia', 'armenia', 'lituania', 'albania', 'jamaica', 'namibia', 'lesoto', 'catar', 'botswana', 'eslovenia', 'letonia', 'gambia', 'guine-bissau', 'kosovo', 'gabao', 'bahrein', 'trinidad e tobago', 'estonia', 'mauricia', 'guine equatorial', 'timor-leste', 'suazilandia', 'djibouti', 'fiji', 'chipre', 'comores', 'butao', 'guiana', 'macau', 'montenegro', 'ilhas salomao', 'luxemburgo', 'suriname', 'cabo verde', 'saara ocidental', 'transnistria', 'malta', 'guadalupe', 'brunei', 'martinica', 'bahamas', 'belize', 'maldivas', 'islandia', 'barbados', 'nova caledonia', 'polinesia francesa', 'vanuatu', 'abecasia', 'guiana francesa', 'mayotte', 'santa lucia', 'guam', 'curacao', 'nagorno-karabakh', 'sao vicente e granadinas', 'aruba', 'kiribati', 'ilhas virgens americanas', 'tonga', 'jersey', 'seychelles', 'antigua e barbuda', 'ilha de man', 'ceuta', 'melilla', 'andorra', 'dominica', 'guernsey', 'bermudas', 'ilhas marshall', 'gronelandia', 'ilhas cayman', 'marianas setentrionais', 'ossetia do sul', 'ilhas faroe', 'sint maarten', 'liechtenstein', 'monaco', 'saint-martin', 'san marino', 'gibraltar', 'ilhas turks e caicos', 'ilhas åland', 'finlandia', 'ilhas virgens britanicas', 'palau', 'bonaire', 'ilhas cook', 'anguilla', 'wallis e futuna', 'tuvalu', 'nauru', 'sao pedro e miquelon', 'montserrat', 'sint eustatius', 'ilhas malvinas', 'svalbard e jan mayen', 'noruega', 'ilha norfolk', 'ilha christmas', 'saba', 'niue', 'tokelau', 'vaticano', 'ilha wake', 'midway atoll', 'ilhas pitcairn']

# Pronoun list
PRONOUNS = ['quem', 'como', 'qual', 'quais', 'quando', 'quanto', 'quantos', 'quantas', 'onde', 'por que', 'por quê']
EXPECTED_ANSWER = {
	
	# TODO: adicionar campo do preposições e nomes para INVALIDAR
	'quem': {
		'regra': ['PREP', 'PROPN'],
		'PREP': ['por', 'para'],
		'PROPN': {}
	},

	'como': '',
	'qual': '',
	'quais': '',
	
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
		'PROPN': {}
	},

	'por que': '',
	'por quê': ''
}


# Load portuguese model
pt_model = spacy.load('pt')
# pergunta = input()
# pergunta = u"Quem é o presidente do Brasil?"
# doc = pt_model(pergunta)

def _find_pron(doc):

	# NOTE: talvez precisemos verificar advérbios, é possível que alguns pronomes 
	# sejam classificados como advérbios (tipo o 'quando': Classe gramatical: 
	# advérbio, conjunção e pronome relativo)
	# Find all pronouns
	prons = [word for word in doc if word.pos_ == 'PRON']
	
	# Process pronoun
	try:
		# Assume that the first pronoun is relative to our question
		pron = prons[0].lower_
		
		# If pronoun is not in our pronoun list, its not a recognizable question
		if not pron in PRONOUNS: raise Exception("Tipo de pergunta não reconhecida")

	except IndexError as e:
		err_msg = "[Error] Nenhum pronome encontrado na pergunta."
		print(err_msg)
		raise ChatbotException(e, err_msg, doc.text)

	except Exception as e:
		err_msg = "[Error] Pronome encontrado ('%s') não está na lista de pronomes suportados." % pron
		print(err_msg)
		raise ChatbotException(e, err_msg, doc.text)

	return pron


def _find_nouns(doc):

	# Process nouns - try to find the question's topic
	nouns = [word for word in doc if word.pos_ == 'NOUN']
	return " ".join([word.lower_ for word in nouns])


def _find_abbreviations(doc):
	return [abbv.text for abbv in doc if abbv.text.isupper()]

def _find_country(doc):

	# Search for Named Entities in doc
	for ent in doc.ents:
		if not "republica" in ent.lower_ and ent.lower_ in COUNTRY_LIST:
			return ent.lower_

	# No valid named entity, fallback
	# Find all proper nouns (country os person names)
	propns = [word for word in doc if word.pos_ == 'PROPN']
	custom_tag = {}

	# Process country name
	try:
		# Assume that the first proper noun is our country name
		propn = propns[0].lower_
		
		# TODO: proper noun can also be a person's name, for now only check for 
		# country's names
		# If our proper noun is not in country's list, its an invalid country
		if not propn in COUNTRY_LIST:
			
			for word in doc:
				if word.lower_ in COUNTRY_LIST:
					custom_tag[word.lower_] = "country"

			try:
				propn = custom_tag.keys()[0]
			except: raise Exception("País desconhecido.")

	except IndexError as e:
		err_msg = "[Error] Nenhum país encontrado na pergunta."
		print(err_msg)
		raise ChatbotException(e, err_msg, doc.text)
	
	except Exception as e:
		err_msg = "[Error] País '%s' desconhecido." % propn
		print(err_msg)
		raise ChatbotException(e, err_msg, doc.text)

	return propn


def parse_question(question, pron=None, country=None, model=pt_model):

	_question = question
	question = text_canonicalize(_question)

	doc = model(question)

	if not pron: pron = _find_pron(doc)
	if not country: country = _find_country(doc)
	abbrvs = _find_abbreviations(doc)
	nouns = _find_nouns(doc)
	topic = nouns + " " + "".join(abbrvs)
	# topic = topic + " " + country

	return {
		"pergunta": _question,
		"pergunta_canon": question,
		"pron": pron,
		"country": country,
		"topic": topic,
		"expected": EXPECTED_ANSWER[pron]
	}


def text_canonicalize(question):

	question = re.sub("[áàâãäåÁÀÂÃÄÅ]", "a", question)
	question = re.sub("[éèêẽëÉÈÊẼË]", "e", question)
	question = re.sub("[íìîĩïÍÌÎĨÏ]", "i", question)
	question = re.sub("[óòôõöÓÒÔÕÖ]", "o", question)
	question = re.sub("[úùûũüÜÚÙÛŨ]", "u", question)
	question = re.sub("[ýỳŷỹÿÝỲŶỸŸ]", "y", question)
	question = re.sub("[çÇ]", "c", question)
	question = re.sub("[ñ]", "n", question)
	return question

def test(path="../perguntas.txt", debug=False):

	file = open(path)
	lines = file.readlines()
	lines = [line.rstrip() for line in lines if line[0] != '#']

	res = []

	for line in lines:
		try:
			if debug: print(line)
			res.append(parse_question(line))

		except ChatbotException as e:
			res.append({"err_msg": "Erro na pergunta '%s'" % line, "exception": e})

		except Exception as e:
			print("Unknown error occured. Error msg: '%s'." % str(e))

	return res
