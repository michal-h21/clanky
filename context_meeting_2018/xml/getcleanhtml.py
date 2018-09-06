import requests
from readability import Document

response = requests.get('https://www.ctrl.blog/entry/browser-reading-mode-parsers')
doc = Document(response.text)
print(doc.title())
print(doc.summary())
