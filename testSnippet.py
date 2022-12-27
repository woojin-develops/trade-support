import requests
import re
from bs4 import BeautifulSoup   
res = requests.get("https://www.bing.com/search?q=%tsla").text
soup = BeautifulSoup(res, "lxml")
scrapes = soup.find("div", {"id":"b_content"}, {})
spec = scrapes.fetchPreviousSiblings
print(scrapes)

