import requests
import colorama
import datetime
import time
import nltk
import itertools
import numpy as np
from bs4 import BeautifulSoup
from itertools import cycle
from collections import defaultdict, Counter
from colorama import Fore
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('punkt')
nltk.download('stopwords')
colorama.init(autoreset=True)
with open('proxies.txt', 'r+', encoding='utf-8') as f:
    proxypool = cycle(f.read().splitlines()) #prevents ratelimits

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
        stop_words = set(stopwords.words('english'))
        tfidf = TfidfVectorizer(stop_words=['the', 'how', 'us', 'may', 'about', 'my', 'also', 'our', 'get', 'by', 'all', 'motley', 'fool', 'really', '2023', '2022', 'said', 'still', 'could'])
        #stemmer = PorterStemmer()
        for symbol in self.symbols:
            for source in self.sources[symbol]:
                corpus = ''
                soup, _ = getNetwork(source)
                main_text = soup.find('body').text
                corpus += main_text
            tokens = nltk.word_tokenize(corpus)
            filtered_tokens = [token for token in tokens if token not in stop_words]
            #stemmed_tokens = [stemmer.stem(token) for token in filtered_tokens]
            tfidf_matrix = tfidf.fit_transform(filtered_tokens)
            feature_names = tfidf.get_feature_names_out()
            tfidf_scores = zip(feature_names, np.asarray(tfidf_matrix.sum(axis=0)).ravel())
            sorted_scores = sorted(tfidf_scores, key=lambda x: x[1], reverse=True)
            important_keywords = [s[0] for s in sorted_scores[:20]]
            print(important_keywords)
    
    def extract_important_sentences(text, n=7):
        soup, _ = getNetwork('https://seekingalpha.com/news/3924446-hexo-stock-extends-gains-rising-volumes')
        main_text = soup.find('body').text
        sentences = nltk.sent_tokenize(main_text)
        #stop_words = set(stopwords.words('english'))
        #filtered_sentences = []
        #for sentence in sentences:
            #filtered_tokens = [token for token in nltk.word_tokenize(sentence) if token not in stop_words]
            #filtered_sentences.append(" ".join(filtered_tokens))
        tfidf = TfidfVectorizer()
        tfidf_matrix = tfidf.fit_transform(sentences)
        feature_names = tfidf.get_feature_names_out()
        tfidf_scores = zip(feature_names, np.asarray(tfidf_matrix.sum(axis=0)).ravel())
        sorted_scores = sorted(tfidf_scores, key=lambda x: x[1], reverse=True)
        sorted_index = (-tfidf_matrix.sum(axis=1)).argsort().tolist()[0][:n]
        important_sentences = [sentences[i] for i in sorted_index]
        print(important_sentences)
def run():
    while True:
        tickers = input('enter stock tickers like tlry, aapl, msft \n')
        if len(tickers) == 0:
            break
        user = Polling(tickers)
        try:
            user.poll()
        except Exception:
            print('ticker(s) could not be found')
        try:
            user.analyze()
        except Exception:
            print('Important keywords could not be found')
        try: 
            user.extract_important_sentences()
        except Exception:
            print('Important sentences could not be found')
        continue
        

        


test = Polling('tlry, msft')
test.poll()
test.analyze()
test.extract_important_sentences
#run()
