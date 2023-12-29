import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import streamlit as st
import streamlit.components.v1 as components
from bs4 import BeautifulSoup
from pathlib import Path
from utils import Predictor

# path settings
bp = Path(__file__).parent / "demodata/buurten.csv"
mp = Path(__file__).parent / "demodata/map/buurt_2020_v3.shp"

st.title('Buurten Vergelijker')
buurt = st.selectbox('Wat is jouw favoriete buurt? Selecteerd hieronder je buurt voor de vergelijker: ',
    ('<select>', 'Oud Hoograven-Zuid', 'Voordorp en Voorveldsepolder', 'Slagen', 'Oorden', 'Poorten'))  

if buurt != '<select>':
    with st.spinner('Even wachten, de kaart wordt geladen...'):
        recommender = Predictor(buurten_path = bp, map_path = mp)
        response = recommender.get_prediction(buurt)
        html_map = BeautifulSoup(response, "html.parser") 

        with open('output.html', 'w', encoding='utf-8') as file:
            file.write(html_map.prettify())        

        with open('output.html', 'r') as f:
            html_map = f.read()

        components.html(html_map, height=600, width=700)
else:
    st.markdown('GWat is jouw favoriete buurt? Selecteerd hieronder je buurt voor de vergelijker:')