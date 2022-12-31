import requests
import colorama
import datetime
import time
import nltk
from bs4 import BeautifulSoup
from itertools import cycle
from collections import defaultdict
from colorama import Fore

colorama.init(autoreset=True)
with open('proxies.txt', 'r+', encoding='utf-8') as f:
    proxypool = cycle(f.read().splitlines()) #useless atm

def getNetwork(URL):
    time.sleep(1)
    res = requests.get(URL).text
    soup = BeautifulSoup(res, 'lxml')
    try:
        price = soup.find('div', {'class':'YMlKec fxKbKc'}).text
    except AttributeError:
        price = None
    return soup, price

class Polling:
    def __init__(self, symbols, exchange = 'nasdaq'):
        self.symbols = [symbol.strip(' ') for symbol in symbols.split(',')]
        self.tickers = [f'https://www.google.com/finance/quote/{symbol}:{exchange}?hl=en' for symbol in self.symbols] 
        self.sources = defaultdict(list)
    def poll(self):
        for URL in self.tickers:
            soup, price = getNetwork(URL)
            ticker = URL.split('/')[5].split(':')[0]
            stock_quotes = soup.find_all('div', {'class':'yY3Lee'})
            if (previous_price := soup.find('div', {'class':'P6K39c'}).text) > price:
                print(f'{Fore.BLUE}{datetime.datetime.now()} {Fore.RED}{ticker} {Fore.GREEN}{previous_price} -----> {Fore.RED}{price}')
            else:
                print(f'{Fore.BLUE}{datetime.datetime.now()} {Fore.GREEN}{ticker} {Fore.RED}{previous_price} -----> {Fore.GREEN}{price}')
            for quote in stock_quotes:
                try:
                    relevancy = quote.find('div', {'class':'Yfwt5'}).text
                    caption = quote.find('div', {'class':'Adak'}).text
                    source = quote.find('div', {'class':'sfyJob'}).text
                    source_link = quote.find('a').get('href')
                except AttributeError:
                    print('AttributeError: NoneType object has no attribute text')
                else:
                    self.sources[f'{ticker}'].append(source_link)
                    print(f'{caption}:{source}:{relevancy}\n{source_link}')
    def analyze(self):
        soup, _ = getNetwork(self.sources['tlry'][0])
        main_text = soup.find('body').text
        tokens = nltk.word_tokenize(main_text)
        print(tokens)
test = Polling('tlry, aapl, msft')
test.poll()
test.analyze()
