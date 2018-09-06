import argparse
import logging
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import cssutils
import requests
from readability import Document

# process CSS files for @import directives
# full css parsing is too slow
class Imports():
    def replace_imports(self, match):
        replacement = ""
        url = match.group(1)
        if url:
            newurl = urljoin(self.url, url)
            csstext = requests.get(newurl)
            if csstext:
                newcss = Imports()
                return newcss.process_css(csstext, newurl)
        return replacement
    # process css text for @import
    def process_css(self, csstext, url):
        self.url = url
        if csstext:
            regex = r"@import.*?[\"']([^\"']+)[\"'].*?;"
            return re.sub(regex, self.replace_imports, csstext) 
        return ""

# don't show css parsing errors and warnings
cssutils.log.setLevel(logging.CRITICAL)
# process all CSS links, style elements and imports and create a one big CSS string
def get_css(dom, baseurl):
    cssutils.ser.prefs.keepComments = False
    cssutils.ser.prefs.lineSeparator = " "
    cssutils.ser.prefs.indent = ' ' 
    csschunks = [] 
    # links should be processed first
    for link in dom.select('link[rel="stylesheet"]'):
        src = link.get("href")
        linkurl = urljoin(baseurl, src)
        print("Download",linkurl)
        csstext = requests.get(linkurl)
        # style = cssutils.parseUrl(linkurl, encoding="utf-8", validate=False)
        print("Parsed, resolve imports")
        newcss = Imports().process_css(csstext.text, linkurl)
        # style = cssutils.resolveImports(style)
        print("Append it")
        csschunks.append(newcss)
        print("processed")
        # print(style.cssText)
    print("".join(csschunks))


url = 'https://knihovna.pedf.cuni.cz/'


soup = BeautifulSoup(requests.get(url).content,features="lxml")

get_css(soup, url)

# css = cssutils.parseUrl(url)

# print(css.cssText)


# response = requests.get(url)
doc = Document(str(soup))
print(doc.title())
print(doc.summary())
