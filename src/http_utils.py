##############################################
# Processamento de Linguagem Natural SCC0633 #
# HTTP handlers and utilities source file    #
#                                            #
# Giovanna Oliveira Guimarães   9293693      #
# Lucas Alexandre Soares        9293265      #
# Rafael Joegs Monteiro         9293095      #
# Darlan Xavier Nascimento      10867851     #
#                                            #
##############################################

import time
import urllib.request, urllib.error 

from selenium import webdriver
from parse_question import text_canonicalize

def url_encode(url):
    url = text_canonicalize(url)
    return url.replace(r" ", r"_")


def get_html(url):
    
    header = "Mozilla/5.001 (windows; U; NT4.0; en-US; rv:1.0) Gecko/25250101"
    
    try:
        request = urllib.request.Request(url)
        request.add_header("User-Agent", header)
        html = urllib.request.urlopen(request).read()
        return html.decode('utf-8')
    
    except urllib.error.HTTPError as e:
        print("Error accessing: ", url)
        if e.code == 503 and 'CaptchaRedirect' in e.read():
            print("Site is requiring a Captcha.")
        return None
    
    except Exception as e:
        print("Error accessing: ", url)
        print(e)
        return None


def get_browser_with_url(url, timeout=120, driver="firefox"):
    """Returns an open browser with a given url."""

    # choose a browser
    if driver == "firefox":
        browser = webdriver.Firefox()
    elif driver == "ie":
        browser = webdriver.Ie()
    elif driver == "chrome":
        browser = webdriver.Chrome()
    else:
        print("Driver choosen is not recognized")

    # set maximum load time
    browser.set_page_load_timeout(timeout)

    # open a browser with given url
    browser.get(url)
    time.sleep(0.5)

    return browser


def write_html_to_file(html, filename):
    of = open(filename, "w")

    of.write(html)
    # of.flush()
    of.close()
