import requests
from bs4 import BeautifulSoup
import csv
import time

BASE_URL = "https://mangialocale.com"
LIST_URL = f"{BASE_URL}/aziende/"

# Header per simulare browser reale
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

def fetch_lista_aziende():
    print("🔍 Recupero elenco aziende...")
    r = requests.get(LIST_URL, headers=HEADERS)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'html.parser')
    links = [a['href'] for a in soup.select('a[href^="/aziende/azienda-agricola-"]')]
    print(f"✅ Trovati {len(links)} link aziendali.")
    return links

def parse_azienda(urlpath):
    url = BASE_URL + urlpath
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'html.parser')

    nome = soup.select_one('h1').get_text(strip=True) if soup.select_one('h1') else ''
    descrizione = soup.select_one('.entry-content').get_text(separator=' ', strip=True) if soup.select_one('.entry-content') else ''
    
    prodotti = [p.get_text(strip=True) for p in soup.select('.woocommerce-Price-amount')]
    
    return {
        'nome': nome,
        'descrizione': descrizione,
        'prodotti_prezzi': '; '.join(prodotti),
        'url': url
    }

def main():
    azienda_links = fetch_lista_aziende()
    dati = []

    for i, path in enumerate(azienda_links, 1):
        try:
            print(f"🔄 [{i}/{len(azienda_links)}] Analisi: {path}")
            data = parse_azienda(path)
            dati.append(data)
            time.sleep(0.5)  # per rispetto verso il server
        except Exception as e:
            print(f"⚠️ Errore su {path}: {e}")

    with open('aziende.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['nome', 'descrizione', 'prodotti_prezzi', 'url'])
        writer.writeheader()
        for row in dati:
            writer.writerow(row)

    print("📁 Dati salvati in aziende.csv")

if __name__ == "__main__":
    main()

