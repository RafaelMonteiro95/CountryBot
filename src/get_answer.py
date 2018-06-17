import sys
import unicodedata
import re
from http_utils import get_html, url_encode
from bs4 import BeautifulSoup
from ChatbotException import ChatbotException

index_mundi_base_url = "https://indexmundi.com/pt/"

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
	country = url_encode(parsed.country)
	url = index_mundi_base_url + country

	html = get_html(url)
	soup = BeautifulSoup(html, "html.parser")

	infobox = soup.findAll("table", attrs={"class": "infobox"})

	try:
		infobox = infobox[0]
	except IndexError as e:
		err_msg = "[Error] Tabela não encontrada"
		print(err_msg)
		raise ChatbotException(e, err_msg, parsed.question)

	infobox = unicodedata.normalize("NFKD", infobox.text)
	infobox = separate_words(infobox)
	infobox_ = re.sub(r"[–−]", r"-", infobox.lower())

	# Debug
	file = open("infobox-brasil.txt", "w")
	file.write(infobox)
	file.close()

	if parsed.core in infobox:
		_, start, end = find_between(infobox_, parsed.core.lower(), " - ")
		print("core")
	else:
		print(parsed.topic.lower())
		_, start, end = find_between(infobox_, parsed.topic.lower(), " - ")

	ans = infobox[start:end]
	
	return ans.strip()