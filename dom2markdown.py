from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import requests
import sys
    
BASE_URL = 'https://www.math.sk/wiki/'
PARAMS = {'action':'show','mimetype':'dom/xml'}

def descend(elem):

    if not elem.tag:
        yield elem.text.strip()
    else:
        for child in elem:
            yield from handle(child)

def handle_p(elem):

    yield '\n'
    yield descend(elem)

def handle_ul(elem):

    for child in elem:
        yield '* '
        yield child.text
        yield '\n'


def handle_hn(elem):

    n=int(elem.tag.split[1:])
    yield '#'*n
    yield elem.text
    yield '\n'

def handle_notag(elem):

    yield elem.text

def handle_default(elem):

    yield from descend(elem)

DISPATCH_CONF={
        ('h1','h2','h3','h4','h5'):handle_hn,
        ('ul',):handle_ul,
        ('p',):handle_p,
        ('',):handle_notag,
}

DISPATCH={}
for key,f in DISPATCH_CONF.items():
    for tag in key:
        DISPATCH[key]=f

def handle(elem):
    
    print('handling',elem.tag,'text',elem.text.strip())
    if elem.tag in DISPATCH:
        yield from DISPATCH[elem.tag]
    else:
        yield from handle_default(elem)


class MoinPage:


    def __init__(self,pagename):

            url = BASE_URL+pagename
            r=requests.get(url,params=PARAMS)
            self.text=r.text
            self.soup=BeautifulSoup(self.text,'lxml')
            for anchor in self.soup.find_all('anchor'):
                anchor.decompose()
            self.et=ET.fromstring(self.soup.prettify())


if __name__=='__main__':

    p=MoinPage('Vyuka')
    print(p.soup)


