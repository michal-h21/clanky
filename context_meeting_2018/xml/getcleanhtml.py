import sys
# import argparse
# import logging
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
from readability import Document
import hashlib
from diskcache import Cache

class UrlCache:
    def __init__(self, path):
        self.path = path
    # get url from cache or url
    def get(self,url):
        byteurl = bytes(url, 'utf-8')
        byteurl = hashlib.sha224(byteurl).hexdigest()
        with Cache(self.path) as cache:
            if byteurl in cache:
                return cache[byteurl]
            else:
                value = requests.get(url)
                cache.add(byteurl, value)
                return value


# process CSS files for @import directives
# full css parsing is too slow
class Imports():
    def replace_imports(self, match):
        replacement = ""
        url = match.group(1)
        if url:
            print("Import CSS", url)
            newurl = urljoin(self.url, url)
            csstext = UrlCache("data").get(newurl)
            # csstext = requests.get(newurl)
            if csstext:
                newcss = Imports()
                return newcss.process_css(csstext, newurl)
        return replacement
    # process css text for @import
    def process_css(self, csstext, url):
        self.url = url
        if csstext and isinstance(csstext, str):
            regex = r"@import.*?[\"']([^\"']+)[\"'].*?;"
            try:
                return re.sub(regex, self.replace_imports, csstext) 
            except:
                print(csstext)

        return ""

class CleanHtml:
    def __init__(self, url):
        self.url = url
        print("Download ", url)
        page_content = requests.get(url).content
        print("Parse DOM")
        self.dom = BeautifulSoup(page_content,features="lxml")
        print("Parse CSS")
        self.css = self.get_css(self.dom, self.url)
        # use full urls for images
        print("Resolve images")
        self.resolve_images()
        print("Remove javascript")
        self.remove_javascript()
        self.template = """
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="utf-8" />
        <title>{}</title>
        <style type="text/css">
        <![CDATA[
        {}
        ]]>
        </style>
        </head>
        <body>
        {}
        </body>
        </html>
        """
    # process all CSS links, style elements and imports and create a one big CSS string
    def get_css(self,dom, baseurl):
        csschunks = [] 
        # links should be processed first
        for link in dom.select('link[rel="stylesheet"]'):
            src = link.get("href")
            linkurl = urljoin(baseurl, src)
            print("Process CSS", linkurl)
            # csstext = requests.get(linkurl)
            csstext = UrlCache("data").get(linkurl)
            # style = cssutils.parseUrl(linkurl, encoding="utf-8", validate=False)
            newcss = Imports().process_css(csstext.text, linkurl)
            # style = cssutils.resolveImports(style)
            csschunks.append(newcss)
            # print(style.cssText)
        for style in dom.select('style[type="text/css"]'):
            print("Process CSS chunk")
            csschunks.append(str(style))
            # remove the style elements so they don't interfere with luaxml
            style.decompose()
        return "".join(csschunks)
    def remove_javascript(self):
        # we don't support scripts
        for script in self.dom.select("script"):
            script.decompose()
    def resolve_images(self):
        for img in self.dom.select("img"):
            img.src = urljoin(self.url, img.get("src"))
            # url = img.get("src")
            # img.set(src=urljoin(self.url, url)
    # hash images url for caching purposes
    def hash_images(self):
        if self.image_hashes:
            for img in self.dom.select("img"):
                print(img)
    def get_clean(self):
        doc = Document(self.dom.prettify(formatter="xml"))
        return self.template.format(doc.title(), self.css, doc.summary(html_partial=True))




url = sys.argv[1]
clean = CleanHtml(url)
# clean.hash_images()
# print(clean.get_clean())

# soup = BeautifulSoup(requests.get(url).content,features="lxml")

# get_css(soup, url)

# css = cssutils.parseUrl(url)

# print(css.cssText)


# response = requests.get(url)
