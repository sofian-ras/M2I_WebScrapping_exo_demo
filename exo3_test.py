from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

# 1
url = "http://books.toscrape.com"
mon_headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

response = requests.get(url,headers=mon_headers)
soup = BeautifulSoup(response.text, "html.parser")

# 2
books_data = []
books = soup.find_all("article", class_="product_pod")

for book in books:
    title = book.h3.a["title"]
    price_text = book.find("p", class_="price_color").text.strip()
    price_text = price_text.replace("£", "").replace("Â", "")
    price = float(price_text)
    rating = book.find("p", class_=re.compile(r"^star-rating"))["class"][1]
    availability = book.find("p", class_="instock availability").text.strip()
    img_src = book.find("img")["src"].replace("../", "")


    books_data.append({
        "title" : title,
        "price" : price,
        "rating" : rating,
        "availability" : availability,
        "image_url" : img_src
    })
# 3
df = pd.DataFrame(books_data)
print("================== : MON DATAFRAME : ==================")
print(df.head())

# 4
prix_moyen = df['price'].mean()
prix_moyen = round(prix_moyen, 2)
print("\n~~~~~~ prix moyen :", prix_moyen, "£")

livre_chere = df.loc[df['price'].idxmax()]
print("\n~~~~~~ livre le PLUS chere :~~~~~~\n",livre_chere)

livre_moin_chere = df.loc[df['price'].idxmin()]
print("\n~~~~~~ livre le MOIN chere :~~~~~~\n",livre_moin_chere)

repartition_note = df['rating'].value_counts()
print("\n ~~~~~~ repartition par note : ~~~~~~")
print(repartition_note)

# 5
df.to_csv("books.csv", index=False)
print("\n//////////// Fichier books.csv enregistré ! ///////////\n")

# Bonus
livre_cher = df.loc[df['price'].idxmax()]
img_url = "http://books.toscrape.com/" + livre_cher['image_url']
livre_max = livre_cher['title'].replace(" ", "_").replace("/", "_")  # nom fichier sûr

img_data = requests.get(img_url).content
with open(f"{livre_max}.jpg", "wb") as f:
    f.write(img_data)

print("Image du livre le plus cher téléchargée !")