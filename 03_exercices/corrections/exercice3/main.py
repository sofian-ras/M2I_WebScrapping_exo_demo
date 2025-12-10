import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
import re

# Configuration
# 1. Récupérer la page d'accueil
url = "http://books.toscrape.com"
response = requests.get(url)
soup = BeautifulSoup(response.text,'lxml')

rating_map = {'One':1,'Two':2,'Three':3,'Four':4,'Five':5}

# trouver tous les livres
books = soup.find_all('article',class_='product_pod')
books_data = []

for book in books:
    title = book.find('h3').find('a')['title']

    price_text = book.find('p', class_='price_color').text
    price = float(re.findall(r'[\d.]+',price_text)[0])

    rating_class = book.find('p',class_='star-rating')['class'][1]
    rating = rating_map.get(rating_class,0)

    availability = book.find('p',class_='instock availability').text.strip()
    in_stock = 'In stock' in availability

    img_url = book.find('img')['src']
    full_img_url = urljoin(url,img_url)

    books_data.append({
        'title' : title,
        'price' : price,
        'rating' : rating,
        'in_stock' : in_stock,
        'image_url' : full_img_url,
    })


# 3. Créer un DataFrame Pandas
df = pd.DataFrame(books_data)
print(df)

# 4. Calculer :
#    - Prix moyen
#    - Livre le plus cher
#    - Livre le moins cher
#    - Répartition par note

print(f"Prix moyen : {df['price'].mean():.2f}")
print(f"Livre le plus cher : {df['price'].max():.2f}")
print(f"Livre le moins cher : {df['price'].min():.2f}")
print("Répartition par note : ")
print(df['rating'].value_counts().sort_index())

df.to_csv('output.csv',index=False)

# Bonus
# Le livre le plus cher
most_expensive = df.nlargest(1,'price').iloc[0]

img_most_expensive = requests.get(most_expensive['image_url'])
with open('mon_image.jpg','wb') as f:
    f.write(img_most_expensive.content)