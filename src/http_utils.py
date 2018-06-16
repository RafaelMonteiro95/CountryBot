from __future__ import unicode_literals
# from __future__ import print_function
# from __future__ import division

from future import standard_library
standard_library.install_aliases()

from selenium import webdriver
from parse_question import text_canonicalize

import time
import urllib.request, urllib.error #, urllib.parse
# from builtins import range
# from past.utils import old_div
# from functools import wraps
# # import requests
# from urllib.parse import urlencode, quote

def url_encode(url):
    url = text_canonicalize(url)
    url.replace(" ", "_")
    return url


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
