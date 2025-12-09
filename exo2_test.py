from bs4 import BeautifulSoup
import requests

url = 'http://quotes.toscrape.com'

# 1
response = requests.get(url)

# 2
soup = BeautifulSoup(response.text, "lxml")

# 3
quotes = soup.select(".quote")

print(quotes)
