import sys
import json
import requests
from bs4 import BeautifulSoup
import unicodedata
from headers import *


def scrape_citations():
    URL = "http://www.values.com/inspirational-quotes"
    r = requests.get(URL)
  
    soup = BeautifulSoup(r.content, 'html5lib')
    #print(r)
  
    quotes=[]  # a list to store quotes
  
    table = soup.find('div', attrs = {'id':'all_quotes'})
    #print(table)
  
    for row in table.findAll('div',
                         attrs = {'class':'col-6 col-lg-4 text-center margin-30px-bottom sm-margin-30px-top'}):
        quote = {}
        #print(row.a['href'])
        quote['theme'] = row.h5.text
        quote['url'] = row.a['href']
        quote['img'] = row.img['src']
        quote['lines'] = row.img['alt'].split(" #")[0]
        quote['author'] = row.img['alt'].split(" #")[1]
        quotes.append(quote)
    #print(quotes)
    return json.dumps(quotes)