import streamlit as st
import pandas as pd
import os

st.title("Aziende – MangiaLocale.com")

csv_path = "aziende.csv"

if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    st.success(f"Trovate {len(df)} aziende.")
    
    search = st.text_input("🔍 Cerca per nome o descrizione").lower()
    if search:
        df = df[df['nome'].str.lower().str.contains(search) | df['descrizione'].str.lower().str.contains(search)]
    
    st.dataframe(df)
else:
    st.warning("Nessun file CSV trovato. Avvia prima `scraper.py` per generarlo.")
