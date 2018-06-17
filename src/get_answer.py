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

from http_utils import get_html, url_encode
from bs4 import BeautifulSoup
from ChatbotException import ChatbotException

index_mundi_base_url = "https://indexmundi.com/pt/"
cache_dir = "cache"
cache_file_base = cache_dir + "/indexmundi-{0}-infobox"

def _cache_webpage(content, filename):
	file = open(filename, "w")
	file.write(content)
	file.flush()
	file.close()

def _get_cached_webpage(filename):
	file = open(filename, "r")
	content = file.read()
	file.close()
	return content

def separate_words(text):
	# Regex for removing extra whitespaces if there is more than one
	remove_whitespace_regex = re.compile(r"\\s+")

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
	result = re.sub(remove_whitespace_regex, r" ", tmp)
	
	return result

def find_between(s, first, last):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end], start, end
    except ValueError:
        return "", 0, 0

'''
def find_between_r( s, first, last ):
    try:
        start = s.rindex( first ) + len( first )
        end = s.rindex( last, start )
        return s[start:end]
    except ValueError:
        return ""
'''

def get_answer(parsed):

	# If cache directory doesnt exists, create it
	if not path.isdir(cache_dir): 
		try:
			makedirs(cache_dir)
		except OSError as e:
			print("[Warning] failed to create cache directory, continuing without cache")
		except Exception as e:
			print("[Error]: Unknown error ocurred. Message: '{0}'".format(str(e)))

	# Check if cached file exists
	cache_file_path = cache_file_base.format(parsed.country.lower())
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
			print("Getting page from cache")
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
			err_msg = "[Error] Tabela não encontrada"
			print(err_msg)
			raise ChatbotException(e, err_msg, parsed.question)

		# Pre-process infobox text
		infobox = unicodedata.normalize("NFKD", infobox.text)
		infobox = separate_words(infobox)
		_cache_webpage(infobox, cache_file_path)
	
	# Generate lowercase infobox for use in comparations
	infobox_ = re.sub(r"[–−]", r"-", infobox.lower())

	# Try searching for answer using question's core first, if no answer, search
	# using topic.
	if parsed.core in infobox:
		_, start, end = find_between(infobox_, parsed.core.lower(), " - ")
	
	# TODO: make better topic searching and processing to get answer
	else:
		_, start, end = find_between(infobox_, parsed.topic.lower(), " - ")

	# Get everything between - blahblah - and assume its the correct answer
	# TODO: clean answer
	ans = infobox[start:end]
	
	return ans.strip()