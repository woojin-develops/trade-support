import requests
from threading import Thread

with open('proxies.txt', 'r+', encoding='utf-8') as f:
    networks = f.read().splitlines()

def getNetwork(networks):
    for network in networks:
        res = requests.get(network).text
        yield res

class Polling:
    def __init__(self):
        self.tickers = []

    def poll(self, symbol):
        pass
