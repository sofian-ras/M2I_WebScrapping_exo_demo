import requests
from bs4 import BeautifulSoup
import json

# config
url = "http://quotes.toscrape.com"
headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# 1. Récupérer la page d'accueil
# 2. Parser avec BeautifulSoup
response = requests.get(url , headers=headers)
soup = BeautifulSoup(response.text,'lxml')

# 3. Trouver toutes les citations (class="quote")
#quotes_elements = soup.select("div.quote")
quotes_elements = soup.find_all("div",class_="quote")
print(f"Nombres de citations : {len(quotes_elements)}") # 6. Compter le nombre total de citations sur la page

# 4. Pour chaque citation, extraire :
#    - Le texte de la citation
#    - L'auteur
#    - Les tags

# 7. Créer une liste de dictionnaires avec les données
quotes_data = []

for quote in quotes_elements:
    #text = quotes_elements.find("span",class_="text").text
    text = quote.find("span",class_="text").text

    author = quote.find("small",class_="author").text
    tags = [tag.text for tag in quote.find_all("a",class_="tag")]

    quotes_data.append({
        'text' : text,
        'author' : author,
        'tags' : tags
    })

# 5. Afficher les 5 premières citations
for i, quote in enumerate(quotes_data[:5],1):
    print(f"{i}) {quote['text']} auteur : {quote['author']} tags : {", ".join(quote["tags"])}")

# 8. **Bonus** : Sauvegarder dans un fichier JSON
with open('output.json','w',encoding='utf-8') as f:
    json.dump(quotes_data,f,indent=4,ensure_ascii=False)