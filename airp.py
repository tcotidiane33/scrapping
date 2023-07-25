
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
    'https://www.airp.ci/fr/liste-officines?page=1',
    'https://www.airp.ci/fr/liste-officines?page=2',
    'https://www.airp.ci/fr/liste-officines?page=3',
    'https://www.airp.ci/fr/liste-officines?page=4',
    'https://www.airp.ci/fr/liste-officines?page=5',
    'https://www.airp.ci/fr/liste-officines?page=6',
    'https://www.airp.ci/fr/liste-officines?page=7',
    'https://www.airp.ci/fr/liste-officines?page=8',
    'https://www.airp.ci/fr/liste-officines?page=9',
    'https://www.airp.ci/fr/liste-officines?page=10',
    'https://www.airp.ci/fr/liste-officines?page=11',
    'https://www.airp.ci/fr/liste-officines?page=12',
    'https://www.airp.ci/fr/liste-officines?page=13',
    'https://www.airp.ci/fr/liste-officines?page=14',
    'https://www.airp.ci/fr/liste-officines?page=15',
    'https://www.airp.ci/fr/liste-officines?page=16',
    'https://www.airp.ci/fr/liste-officines?page=17',
    'https://www.airp.ci/fr/liste-officines?page=18',
    'https://www.airp.ci/fr/liste-officines?page=19',
    'https://www.airp.ci/fr/liste-officines?page=20',
    'https://www.airp.ci/fr/liste-officines?page=21',
    'https://www.airp.ci/fr/liste-officines?page=22',
    'https://www.airp.ci/fr/liste-officines?page=23',
    'https://www.airp.ci/fr/liste-officines?page=24',
    'https://www.airp.ci/fr/liste-officines?page=25',
    'https://www.airp.ci/fr/liste-officines?page=26',
    'https://www.airp.ci/fr/liste-officines?page=27',
    'https://www.airp.ci/fr/liste-officines?page=28',
    'https://www.airp.ci/fr/liste-officines?page=29',
    'https://www.airp.ci/fr/liste-officines?page=30',
    'https://www.airp.ci/fr/liste-officines?page=31',
    'https://www.airp.ci/fr/liste-officines?page=32',
    'https://www.airp.ci/fr/liste-officines?page=33',
    'https://www.airp.ci/fr/liste-officines?page=34',
    'https://www.airp.ci/fr/liste-officines?page=35',
    'https://www.airp.ci/fr/liste-officines?page=36',
    'https://www.airp.ci/fr/liste-officines?page=37',
    'https://www.airp.ci/fr/liste-officines?page=38',
    'https://www.airp.ci/fr/liste-officines?page=39',
    'https://www.airp.ci/fr/liste-officines?page=40',
    'https://www.airp.ci/fr/liste-officines?page=41',
    'https://www.airp.ci/fr/liste-officines?page=42',
    'https://www.airp.ci/fr/liste-officines?page=43',
    'https://www.airp.ci/fr/liste-officines?page=44',
    'https://www.airp.ci/fr/liste-officines?page=45',
    'https://www.airp.ci/fr/liste-officines?page=46',
    'https://www.airp.ci/fr/liste-officines?page=47',
    'https://www.airp.ci/fr/liste-officines?page=48',
    'https://www.airp.ci/fr/liste-officines?page=49',
    'https://www.airp.ci/fr/liste-officines?page=50',
    'https://www.airp.ci/fr/liste-officines?page=51',
    'https://www.airp.ci/fr/liste-officines?page=52',
    'https://www.airp.ci/fr/liste-officines?page=53',
    'https://www.airp.ci/fr/liste-officines?page=54',
    'https://www.airp.ci/fr/liste-officines?page=55',
    'https://www.airp.ci/fr/liste-officines?page=56',
    'https://www.airp.ci/fr/liste-officines?page=57',
    'https://www.airp.ci/fr/liste-officines?page=58',
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
df.to_excel('airpcidata.xlsx', index=False)
