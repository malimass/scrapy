import io

import pandas as pd
import requests
import streamlit as st

from sgr_batterie_scraper import (
    USER_AGENT,
    flatten_products,
    iter_battery_products,
)

st.set_page_config(page_title="SGR Batterie Scraper", layout="wide")
st.title("SGR Batterie Scraper")
st.write("Inserisci URL ricerca e avvia lo scraping direttamente da browser.")

search_url = st.text_input(
    "URL ricerca SGR",
    "https://www.sgr-it.com/it/ricerca.html?token=4l9xBlXKKZogYxWGDKXcesdZJWMQMDkPpmdxx1ZP6C2y48jwTDS0fq5OmkAO",
)
timeout = st.number_input("Timeout richieste (secondi)", min_value=5, max_value=120, value=30)
no_proxy = st.checkbox("Disabilita proxy di sistema", value=False)

if st.button("Avvia scraping", type="primary"):
    try:
        session = requests.Session()
        session.headers.update({"User-Agent": USER_AGENT})
        if no_proxy:
            session.trust_env = False

        with st.spinner("Scarico e analizzo i prodotti..."):
            products = list(iter_battery_products(session, search_url, timeout=int(timeout)))
            rows = flatten_products(products)

        if not rows:
            st.warning("Nessun prodotto batteria trovato.")
        else:
            df = pd.DataFrame(rows)
            st.success(f"Trovati {len(df)} prodotti batteria")
            st.dataframe(df, use_container_width=True)

            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            st.download_button(
                "Scarica CSV",
                data=csv_buffer.getvalue(),
                file_name="batterie_sgr.csv",
                mime="text/csv",
            )
    except Exception as exc:
        st.error(f"Errore durante lo scraping: {exc}")

st.markdown("### Avvio")
st.code("streamlit run scraper_browser_app.py", language="bash")
