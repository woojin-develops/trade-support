import requests
import colorama
import datetime
import time
from bs4 import BeautifulSoup
from colorama import Fore
from requests import Session


colorama.init(autoreset=True)
with open('proxies.txt', 'r+', encoding='utf-8') as f:
    proxies = f.read().splitlines() #useless atm

def getNetwork(URL):
    time.sleep(1)
    res = requests.get(URL).text
    soup = BeautifulSoup(res, 'lxml')
    price = soup.find('div', {'class':'YMlKec fxKbKc'}).text
    return soup, price

class Polling:
    def __init__(self, symbols, exchange = 'nasdaq'):
        symbols = [symbol.strip(' ') for symbol in symbols.split(',')]
        self.tickers = [f'https://www.google.com/finance/quote/{symbol}:{exchange}?hl=en' for symbol in symbols] 
    
    def poll(self):
        for URL in self.tickers:
            soup, price = getNetwork(URL)
            ticker = URL.split('/')[5].split(':')[0]
            if (previousPrice:=soup.find('div', {'class':'P6K39c'}).text) > price:
                print(f'{datetime.datetime.now()}{Fore.RED}{ticker} {Fore.GREEN}{previousPrice} -----> {Fore.RED}{price}')
            else:
                print(f'{datetime.datetime.now()}{Fore.GREEN}{ticker} {Fore.RED}{previousPrice} -----> {Fore.GREEN}{price}')
            stockQuotes = soup.find_all('div', {'class':'yY3Lee'})
            for quote in stockQuotes:
                try:
                    relevancy = quote.find('div', {'class':'Yfwt5'}).text
                    caption = quote.find('div', {'class':'Adak'}).text
                    source = quote.find('div', {'class':'sfyJob'}).text
                    sourceLink = quote.find('a').get('href')
                except AttributeError:
                    print('AttributeError: NoneType object has no attribute text')
                else:
                    print(f'{caption}:{source}:{relevancy}\n{sourceLink}')
