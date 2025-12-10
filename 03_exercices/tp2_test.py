from bs4 import BeautifulSoup
import requests
import time

# --- Initialisation ---
base_url = "https://quotes.toscrape.com"
url = base_url              # URL de départ
next_url = True             # Variable pour contrôler la boucle
page_count = 1              # Initialisation du compteur à 1 (on est déjà sur la première page)

print("Démarrage du calcul du nombre de pages...")

while next_url:
    
    # 1. Requête et Parsing de l'URL actuelle
    # NOTE: Dans un vrai scénario, il serait plus efficace de ne pas refaire la requête 
    # de la page 1 si elle a déjà été faite avant la boucle.
    # Mais ici, on garde la requête à l'intérieur pour une boucle propre et complète.
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # 2. Vérifier s'il y a une page suivante
    next_page_element = soup.find('li', class_='next')
    
    if next_page_element:
        # S'il y a un lien "Next", on récupère l'attribut 'href'
        relative_url = next_page_element.find('a')['href']
        
        # On construit la nouvelle URL pour la prochaine itération
        url = base_url + relative_url
        
        # On incrémente le compteur de page
        page_count += 1
        
        # Politesse de scraping : attendre une seconde avant la prochaine requête
        # Pour une simple détection, on peut le rendre très court (ex: 0.1s)
        time.sleep(0.1) 
        
    else:
        # S'il n'y a plus d'élément 'next', c'est la dernière page. On arrête la boucle.
        next_url = False

print("-" * 40)
print(f" La dernière page atteinte est la Page {page_count}.")
print(f"Il y a donc un total de {page_count} pages à scraper sur ce site.")

##############################################################################################################

# --- Initialisation ---
base_url = "https://quotes.toscrape.com"
url = base_url # URL de départ
all_quotes = [] # Liste pour stocker tous les résultats
page_count = 0  # Compteur pour limiter à 10 pages

# La première requête/soup dans votre code initial est désormais gérée dans la boucle
next_url = True # Indicateur de boucle

print("Démarrage du scraping multi-pages...")
print("-" * 40)

while next_url and page_count < 10:
    
    # 1. Requête et Parsing de l'URL actuelle
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    page_count += 1
    print(f"Extraction des données de la Page {page_count} : {url}")

    # 2. Extraction des données (NOUVELLE SECTION)
    # Trouver tous les blocs de citations
    quotes_on_page = soup.find_all('div', class_='quote')

    for quote_tag in quotes_on_page:
        # Extraire le texte, l'auteur et les tags
        text = quote_tag.find('span', class_='text').text.strip()
        author = quote_tag.find('small', class_='author').text.strip()
        
        # Récupération des tags dans une liste
        tags = [tag.text.strip() for tag in quote_tag.find('div', class_='tags').find_all('a', class_='tag')]
        
        all_quotes.append({
            'text': text,
            'author': author,
            'tags': tags
        })
    
    # 3. Vérifier s'il y a une page suivante (Votre Logique de Pagination)
    next_page_element = soup.find('li', class_='next')
    
    if next_page_element and page_count < 10:
        # Si un lien "Next" existe ET que nous n'avons pas atteint la limite de 10
        relative_url = next_page_element.find('a')['href']
        
        # On construit la nouvelle URL pour la prochaine itération
        url = base_url + relative_url
        
        # Politesse de scraping : attendre une seconde avant la prochaine requête
        time.sleep(1)
        
    else:
        # S'il n'y a plus d'élément 'next' ou si nous avons atteint la page 10
        next_url = False
        print("-" * 40)
        print(" Fin du scraping (dernière page atteinte, limite de 10 pages respectée).")

print(f"Nombre total de citations récupérées : {len(all_quotes)}")