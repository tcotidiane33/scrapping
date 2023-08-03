
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import time



def scrape_page(url):
    # Faire une requête HTTP au site web
    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.text
    else:
        print(f'Erreur lors de la requête HTTP pour {url}.')
        return None

    # Analyser le contenu HTML avec Beautiful Soup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Trouver toutes les lignes du tableau (balise tr avec la classe "odd" ou "even")
    rows = soup.find_all('tr', class_=['odd', 'even'])

    # Initialiser une liste pour stocker les données extraites
    table_data = []

    # Parcourir chaque ligne du tableau
    for row in rows:
        # Extraire les cellules de chaque ligne (balises td)
        cells = row.find_all('td')

        # Extraire les informations que vous souhaitez de chaque cellule (utilisez les méthodes de Beautiful Soup)
        colonne1 = cells[0].text.strip()
        colonne2 = cells[1].text.strip()
        colonne3 = cells[2].text.strip()

        # Ajouter les informations dans un dictionnaire
        data = {
            'PHARMACIES': colonne1,
            'DOCTEUR': colonne2,
            'GEOLOCALISATION & COORDONNEE': colonne3
        }

        # Ajouter le dictionnaire à la liste
        table_data.append(data)

    return table_data

# Liste des URLs des pages de pagination
pages = [
    'https://www.airp.ci/fr/liste-officines?term_node_tid_depth=12',
    'https://www.airp.ci/fr/liste-officines?term_node_tid_depth=12&page=1',
    'https://www.airp.ci/fr/liste-officines?term_node_tid_depth=12&page=2',
    'https://www.airp.ci/fr/liste-officines?term_node_tid_depth=12&page=3',
    'https://www.airp.ci/fr/liste-officines?term_node_tid_depth=12&page=4',
    'https://www.airp.ci/fr/liste-officines?term_node_tid_depth=12&page=5',
    
]


# Initialiser une liste pour stocker toutes les données de toutes les pages
all_data = []

# Afficher un message d'information
print("Lancement du scrapping en cours...")

# Utiliser tqdm pour la barre de progression
for page_url in tqdm(pages):
    data = scrape_page(page_url)
    if data:
        all_data.extend(data)
    # Mettre une petite pause pour éviter de surcharger le serveur
    time.sleep(1)

# Afficher un message de fin avec les remerciements de l'entreprise Kondronetworks
print("Le scrapping est terminé ! Merci de votre patience. - Kondronetworks")

# Créer un DataFrame à partir de la liste de dictionnaires de toutes les pages
df = pd.DataFrame(all_data)

# Enregistrer les données dans un fichier Excel
df.to_excel('Abobo.xlsx', index=False)
