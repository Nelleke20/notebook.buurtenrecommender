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
# img = Path(__file__).parent / "img/lookalike.png"

st.title('Buurten Vergelijker')
buurt = st.selectbox('Selecteer hieronder je favo-buurt: ',
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

        if html_map:
            st.markdown('Viola, de volgende 3 buurten lijken op jouw favoriet: ')
            # components.html(html_map, height=350, width=350) # tel
            components.html(html_map, height=600, width=700) # web

else:
    st.markdown('Wat is jouw favoriete buurt? Selecteer je buurt en de vergelijker doet zijn werk...')
    # st.image(image=img, caption="Buurten Vergelijker")
    