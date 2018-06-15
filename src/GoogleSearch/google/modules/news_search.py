from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from future import standard_library
standard_library.install_aliases()
from builtins import range
from builtins import object
from .utils import _get_news_search_url, get_html
from bs4 import BeautifulSoup
import urllib.parse
from urllib.parse import unquote
from unidecode import unidecode

from past.utils import old_div
import urllib.request, urllib.error, urllib.parse
from urllib.parse import urlencode, quote

import re
import lxml.html
import pdb

class GoogleNewsResult(object):

    """Represents a google search result."""

    def __init__(self):
        self.title = None  # The title of the link
        self.link = None  # The external link
        self.related = None  # Terms related to the link

        self.google_link = None  # The google link
        self.thumb = None  # Thumbnail link of website (NOT implemented yet)
        self.page = None  # Results page this one was on
        self.index = None  # What index on this page it was on
        self.date = None  # What date this page was indexed by Google
        self.content = None  # Content

    def __repr__(self):
        title = self._limit_str_size(self.title, 55)

        list_google = ["GoogleNewsResult(",
                       "title={}".format(title), "\n", " " * 13,]

        return "".join(list_google)

    def _limit_str_size(self, str_element, size_limit):
        """Limit the characters of the string, adding .. at the end."""
        if not str_element:
            return None

        elif len(str_element) > size_limit:
            return unidecode(str_element[:size_limit]) + ".."

        else:
            return unidecode(str_element)


# PUBLIC
def search_news(query, pages=1, lang='pt-BR', region='br', void=True):
    """Returns a list of GoogleNewsResult.

    Args:
        query: String to search in google.
        lang: Which idiom should google search by.
        region: Which country should the search prioritize.

    Returns:
        A GoogleNewsResult object."""
    
    # pages: Number of pages where results must be taken. Not supported anymore

    url_regex = '("https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}([-a-zA-Z0-9@:%_\+.~#?&//=\\\\]*)",( |\n|\t)*".*")'

# url_regex = '("https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}([-a-zA-Z0-9@:%_\+.~#?&//=\\\\]*)",( |\n|\t)*".*")'
# regex = re.compile(url_regex)
# urls = regex.findall(script)

    epoch_time_regex = '[0-9]{13}'

    regex = re.compile(url_regex)
    time_regex = re.compile(epoch_time_regex)
    results = []
    
    for i in range(pages):
        url = _get_news_search_url(query, lang=lang, region=region, sortby='r')
        url = url.decode("utf-8")
        # print("Got url: " + url)
        # print()

        html = get_html(url)
        # print("HTML: " + html.decode("utf-8"))
        # print()

        if html:
            # Google news classes are hashes, dont trust them
            soup = BeautifulSoup(html, "html.parser")

            # c_wizs = soup.findAll("c-wiz", attrs={"class": "M1Uqc MLSuAf"})
            script = soup.body.findAll("script", recursive = False)

            script = script[-2] # The script containing news info is before last one
            script = script.decode_contents() # Get inner html as string

            urls = regex.findall(script)
            times = time_regex.findall(script)
            
            for j in range(len(urls)):
                res = GoogleNewsResult()

                res.page = i
                res.index = j

                res.link = _get_link(urls[j])
                res.title = _get_title(urls[j])
                 
                # res.related = _get_related_terms(li) TODO
                res.google_link = url
                # res.thumb = _get_thumb(li) not working
                res.date = times[j] # Get date
                
                # if void is True:
                #     if res.description is None:
                #         continue
                results.append(res)

    return results

def get_html(url):
    header = "Mozilla/5.001 (windows; U; NT4.0; en-US; rv:1.0) Gecko/25250101"
    try:
        request = urllib.request.Request(url)
        request.add_header("User-Agent", header)
        html = urllib.request.urlopen(request).read()
        return html
    except urllib.error.HTTPError as e:
        print("Error accessing: ", url)
        if e.code == 503 and 'CaptchaRedirect' in e.read():
            print("Google is requiring a Captcha. " \
                  "For more information see: 'https://support.google.com/websearch/answer/86640'")
        return None
    except Exception as e:
        print("Error accessing: ", url)
        print(e)
        return None

def get_content(html):
    
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "sup"]):
        tag.extract()

    tags_to_remove = list()
    tags_to_remove.append(soup.findAll("div", attrs={"class": "hatnote"}))
    tags_to_remove.append(soup.findAll("div", attrs={"class": "thumb tright"}))
    tags_to_remove.append(soup.findAll("div", attrs={"class": "thumb tleft"}))
    tags_to_remove.append(soup.findAll("div", attrs={"class": "thumbinner"}))

    for rset in tags_to_remove:
        for tag in rset:
            try:
                tag.decompose()
            except: # Tag may already have been removed if it was inside another tag
                pass 

    parser_content = soup.findAll("div", attrs={"class": "mw-parser-output"})

    for pcontent in parser_content:

        content = ''
        for div in pcontent:
            content += str(div).strip()

        content = re.sub(r'<[^>]*>', " ", content)
        content = re.sub(r'[©º•😮ª×↑«»·]+', " ", content)
        # content = re.sub(r'[ \'`~^“”",;:?!.@#$€*\-_+={}\[\]\(\)/%&–|©º•😮ª×″↑«»·]+', " ", content)
        # content = re.sub(r'\b[a-zA-Z]\b', " ", content)
        # content = re.sub(r'[ \s\r\n\t]+', " ", content)
        # content = content.lower()
    
    return content

# PRIVATE
def _get_title(urls):
    """Return the title of the new."""
    return re.split(',', urls[0].replace('"', ''))[1]


def _get_link(urls):
    """Return external link from a search."""
    return re.split(',', urls[0].replace('"', ''))[0]


def _get_google_link(urls):
    """Return google link from a search."""
    try:
        a = urls.find("a")
        link = a["href"]
    except:
        return None

    if link.startswith("/url?") or link.startswith("/search?"):
        return urlparse.urljoin("http://www.google.com", link)

    else:
        return None


def _get_related_terms(urls):
    
    try:
        a = urls.find(attrs={'class': 'lPV2Xe k3Pzib RbLfob'})
    except Exception:
        return None


def _get_thumb(urls):
    """Return the link to a thumbnail of the website."""
    print("getting thumbnail link")
    try:
        link = urls["data-thumbnail-url"]
        return link
    except Exception:
        return None
        
