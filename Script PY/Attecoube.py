import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import time
import re

import re

def extract_phone_and_location(content):
    # Définir le modèle d'expression régulière pour les numéros de téléphone
    telephone_pattern = r'\+\d{2,}(?:\s?\d+)*(?:\s?[\/-]?\s?\+\d{2,}(?:\s?\d+)*)*'

    # Trouver tous les numéros de téléphone dans la chaîne
    telephones = re.findall(telephone_pattern, content)

    # Définir le modèle d'expression régulière pour les adresses de géolocalisation (commençant par des lettres)
    geolocalisation_pattern = r'[A-Za-z].*'

    # Chercher la correspondance pour les adresses de géolocalisation dans la chaîne
    geolocalisation_match = re.search(geolocalisation_pattern, content)

    if geolocalisation_match:
        # Extraire l'adresse de géolocalisation
        geolocalisation = geolocalisation_match.group()
    else:
        geolocalisation = ''

    return telephones, geolocalisation.strip()

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

        # Extraire les numéros de téléphone et la géolocalisation en utilisant la fonction extract_phone_and_location
        telephones, geolocalisation = extract_phone_and_location(colonne3)

        # Ajouter les informations dans un dictionnaire
        data = {
            'PHARMACIES': colonne1,
            'DOCTEUR': colonne2,
            'TELEPHONES': telephones,  # Concaténer les numéros de téléphone s'il y en a plusieurs
            'GEOLOCALISATION': geolocalisation
        }

        # Ajouter le dictionnaire à la liste
        table_data.append(data)

    return table_data

# Liste des URLs des pages de pagination
pages = [
    'https://www.airp.ci/fr/liste-officines?term_node_tid_depth=14',
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

# Enregistrer les données dans un unique fichier Excel
df.to_excel('Attecoube.xlsx', index=False)
