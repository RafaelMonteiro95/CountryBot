##############################################
# Processamento de Linguagem Natural SCC0633 #
# Answer retrieval source file               #
#                                            #
# Giovanna Oliveira Guimarães   9293693      #
# Lucas Alexandre Soares        9293265      #
# Rafael Joegs Monteiro         9293095      #
# Darlan Xavier Nascimento      10867851     #
#                                            #
##############################################


import sys
import unicodedata
import re


from os import path, makedirs
from datetime import datetime
from itertools import permutations
from bs4 import BeautifulSoup

from http_utils import get_html, url_encode
from ChatbotException import ChatbotException
from parse_question import pt_model, text_canonicalize


index_mundi_base_url = "https://indexmundi.com/pt/"
cache_dir = "cache"
cache_file_base = cache_dir + "/indexmundi-{0}-infobox"

def _cache_webpage(content, filename):
	file = open(filename, "w", encoding="utf8")
	file.write(content)
	file.flush()
	file.close()

def _get_cached_webpage(filename):
	file = open(filename, "r", encoding="utf8")
	content = file.read()
	file.close()
	return content

def _process_answer(ans):

	start = 0
	end = 0
	counter = 0
	
	in_paren = False
	in_sbrack = False

	# Find first word index
	for i in ans:
		if i == "(": in_paren = True
		elif i == ")": in_paren = False
		elif i == "[": in_sbrack = True
		elif i == "]": in_sbrack = False
		
		elif not in_paren and not in_sbrack and i.isalnum():
			start = counter
			break

		counter += 1

	# Find some possible separators like [], (), \n...
	counter = 0

	for i in ans[start:]:
		if i == " ": pass # ignore whitespace
		elif not i.isprintable() or i == '[' or i == '-':
		#or not i.isalnum():
			end = counter
			break
		counter += 1

	return ans[start:end] if start < end else ans

def remove_extra_whitespace(text):
	# Regex for removing extra whitespaces if there is more than one
	remove_whitespace_regex = re.compile(r"\\s+")
	return re.sub(remove_whitespace_regex, r" ", text)
	

def separate_words(text):

	# Regexes used to identify words that comes BEFORE the type of words we want to
	# separate
	word_regex = r"[\)\]a-z]"
	year_regex = r"\d{4}"
	phone_regex = r"telef\."
	phone_code_regex = r"\+\d+"

	# Final regex used to identify trailing words
	trailing_words_regex = r"({0}|{1}|{2}|{3})".format(word_regex, year_regex, phone_regex, phone_code_regex)

	# Regexes used to identify words that comes AFTER the type of words we want to
	# separate
	alphanumeric_regex = r"[A-Z0-9\[]"
	gov_site_regex = r"www\.\w+\.gov"

	# Final regex used to identify heading words
	heading_words_regex = r"({0}|{1}|{2})".format(alphanumeric_regex, gov_site_regex, phone_code_regex)

	# Compose them
	final_regex = trailing_words_regex + heading_words_regex

	# Separate words
	tmp = re.sub(final_regex, r"\1 \2", text)

	# Remove extra whitespaces
	result = remove_extra_whitespace(tmp)
	
	return result

def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end], start, end
    except ValueError:
        return "", 0, 0

def get_answer(parsed):

	# If cache directory doesnt exists, create it
	if not path.isdir(cache_dir): 
		try:
			makedirs(cache_dir)
		except OSError as e:
			print("[Warning] Falha ao criar o diretório de cache, continuando sem cache")
		except Exception as e:
			print("[Error]: Erro desconhecido. Mensagem: '{0}'".format(str(e)))

	# Check if cached file exists
	try:
		cache_file_path = cache_file_base.format(parsed.country.lower())
	except AttributeError as e:
		err_msg = "[Error] Nenhum país fornecido, impossível encontrar uma resposta."
		raise ChatbotException(e, err_msg, parsed.question)

	cache_need_update = True

	if path.isfile(cache_file_path):

		# Check cached file timestamp
		cache_timestamp = datetime.fromtimestamp(path.getmtime(cache_file_path))
		diff = datetime.now() - cache_timestamp
		
		# If file is more than 1 day old, update it, else just load file
		if diff.days > 0:
			cache_need_update = True
		else: 
			cache_need_update = False
			infobox = _get_cached_webpage(cache_file_path)
	
	# No cache or cache needs update, download file
	if cache_need_update:
		
		# Create url for indexmundi
		country = url_encode(parsed.country)
		url = index_mundi_base_url + country

		html = get_html(url)
		soup = BeautifulSoup(html, "html.parser")

		# Find infobox table
		infobox = soup.findAll("table", attrs={"class": "infobox"})

		try:
			infobox = infobox[0]
		except IndexError as e:
			# NOTE: a página do kiribati não existe
			# NOTE: a do Vietnã deve ser vietname
			err_msg = "[Error] Tabela não encontrada"
			raise ChatbotException(e, err_msg, parsed.question)

		# Pre-process infobox text
		# IMPORTANT: NÃO REMOVER O K DA NORMALIZAÇÃO!!!!!! VAI CAGAR TUDO, PARECE UMA BOA IDEIA NA HORA, MAS DEPOIS VAI SER PIOR!
		infobox = unicodedata.normalize("NFKC", infobox.text)
		infobox = separate_words(infobox)
		# infobox = re.sub(r"\n", r" ", infobox.lower())
		_cache_webpage(infobox, cache_file_path)
	
	# Generate lowercase infobox for use in comparations
	# TODO: use spacy idx 
	infobox_ = re.sub(r"[-–−]", r"-", infobox.lower())
	infobox_model = pt_model(infobox)
	canon_infobox_model = pt_model(infobox)
	unstoppable_infobox = " ".join([word.text for word in infobox_model if word.is_stop == False])
	canon_unstoppable_infobox = " ".join([word.text for word in canon_infobox_model if word.is_stop == False])

	# print(unstoppable_infobox, "\n\n", canon_unstoppable_infobox)
	
	ans = None

	# Try searching for answer using question's core first, if no answer, search
	# using topic.
	# IMPORTANT: this isnt working and i dunno why, halp
	# if parsed.core in infobox:
	# 	_, start, end = find_between(infobox_, parsed.core.lower(), " - ")
	# 	# Get everything between - blahblah - and assume its the correct answer
	# 	# TODO: clean answer
	# 	ans = infobox[start:end]

	# No answer found with core, search with topic
	if not ans and parsed.topic:
		perm = permutations(parsed.topic.lower().split(" "))
		for p in perm:
			query = " ".join(p)
			# print(repr(query))
			_, start, end = find_between(canon_unstoppable_infobox.lower(), query, " - ")
			ans = unstoppable_infobox[start:end]
			if ans: break

	if not ans:
		return 'Topic not Found'

	ans = _process_answer(re.sub(r"[-–−]", r"-", ans))

	return ans.strip()