import requests
from bs4 import BeautifulSoup
import csv
import time

BASE_URL = "https://mangialocale.com"
LIST_URL = f"{BASE_URL}/aziende/"

def fetch_lista_aziende():
    r = requests.get(LIST_URL)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'html.parser')
    # seleziona i link alle singole aziende
    return [a['href'] for a in soup.select('a[href^="/aziende/azienda-agricola-"]')]

def parse_azienda(urlpath):
    url = BASE_URL + urlpath
    r = requests.get(url)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'html.parser')
    # Estrai nome
    nome = soup.select_one('h1').get_text(strip=True) if soup.select_one('h1') else ''
    # Estrai descrizione o prodotti principali
    descrizione = soup.select_one('.entry-content').get_text(separator=' ', strip=True) if soup.select_one('.entry-content') else ''
    # Estrai prodotti con prezzi se desiderato
    prodotti = []
    for item in soup.select('.woocommerce-Price-amount'):
        prodotti.append(item.get_text(strip=True))
    return {
        'nome': nome,
        'descrizione': descrizione,
        'prodotti_prezzi': '; '.join(prodotti),
        'url': url
    }

def main():
    azienda_links = fetch_lista_aziende()
    print(f"Trovate {len(azienda_links)} aziende.")
    dati = []
    for path in azienda_links:
        try:
            data = parse_azienda(path)
            dati.append(data)
            time.sleep(0.5)
        except Exception as e:
            print(f"Errore su {path}: {e}")

    # Salva CSV
    fieldnames = ['nome', 'descrizione', 'prodotti_prezzi', 'url']
    with open('aziende.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in dati:
            writer.writerow(row)

if __name__ == "__main__":
    main()
