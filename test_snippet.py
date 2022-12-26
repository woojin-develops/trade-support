from bs4 import BeautifulSoup
import requests
website = "https://www.cnn.com/search?q=tsla&sort=newest&from=0&size=10&page=1&types=all&section="
res = requests.get(website).text
soup = BeautifulSoup(res, 'html.parser')
matching = soup.find('div', {'data-uri':''}, {'class': 'card container__item container__item--type- __item __item--type- '}, {'data-unselectable':'true'})
print(matching)


                                                                                                                                         