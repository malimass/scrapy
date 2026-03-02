# SGR Batterie Scraper

Questo repository contiene:
- `sgr_batterie_scraper.py`: scraper CLI per estrarre prodotti batteria dal sito SGR.
- `scraper_browser_app.py`: interfaccia Streamlit per lanciare lo scraping da browser.

## Avvio da browser tramite GitHub Codespaces

Se vuoi usarlo **direttamente da browser partendo da GitHub**:

1. Apri il repository su GitHub.
2. Clicca **Code** → **Codespaces** → **Create codespace on main** (o branch desiderato).
3. Nel terminale del Codespace esegui:

```bash
pip install -r requirements.txt
streamlit run scraper_browser_app.py --server.address 0.0.0.0 --server.port 8501
```

4. Quando appare la porta `8501`, clicca **Open in Browser**.
5. Si aprirà la UI Streamlit: inserisci URL ricerca e premi **Avvia scraping**.

## Avvio da browser con Streamlit Community Cloud

Alternativa senza Codespaces:

1. Pusha il repository su GitHub.
2. Vai su [share.streamlit.io](https://share.streamlit.io/).
3. Crea una nuova app selezionando:
   - repository GitHub
   - branch
   - file principale: `scraper_browser_app.py`
4. Deploy.

L'app sarà accessibile via URL pubblico nel browser.

## Esecuzione locale rapida

```bash
pip install -r requirements.txt
streamlit run scraper_browser_app.py
```

Poi apri `http://localhost:8501`.

## Risoluzione errore GitHub: "Can’t automatically merge"

Se in GitHub vedi il messaggio **"Can’t automatically merge"**, significa che il tuo branch e il branch di destinazione (di solito `main`) hanno modificato le stesse righe.

### Opzione 1 (consigliata): risolvi da command line

```bash
git fetch origin
git checkout <tuo-branch>
git merge origin/main
```

Se compaiono conflitti:
1. Apri i file con marker `<<<<<<<`, `=======`, `>>>>>>>`.
2. Tieni il contenuto corretto.
3. Poi esegui:

```bash
git add .
git commit -m "Resolve merge conflicts with main"
git push origin <tuo-branch>
```

A questo punto GitHub ricalcola la PR e il merge automatico torna disponibile.

### Opzione 2: risolvi da web editor GitHub

Quando GitHub mostra il bottone **Resolve conflicts**:
1. Clicca **Resolve conflicts**.
2. Modifica il file conflittuale.
3. Clicca **Mark as resolved**.
4. Crea il commit di risoluzione dal browser.

### Verifica rapida locale prima del push

```bash
python -m unittest discover -s tests -v
python -m py_compile sgr_batterie_scraper.py scraper_browser_app.py
```
