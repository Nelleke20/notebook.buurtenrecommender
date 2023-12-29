import streamlit as st
import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ssl
from streamlit_folium import folium_static
import geopandas as gpd
ssl._create_default_https_context = ssl._create_unverified_context
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import streamlit.components.v1 as components
import requests
import html
from bs4 import BeautifulSoup

# settings that can be altered (possible through a form in streamlit but for now only here)
provincie_utrecht_gemeente =['Amersfoort','Baarn', 'Bunnik', 'Bunschoten', 'De Bilt',
    'De Ronde Venen','Eemnes','Houten', 'Leusden', 'Lopik', 'Montfoort', 'Nieuwegein',
    'Oudewater','Renswoude', 'Rhenen', 'Soest', 'Stichtse Vecht', 'Utrecht', 'Utrechtse Heuvelrug',
    'Veenendaal', 'Vijfheerenlanden', 'Wijk bij Duurstede', 'Woerden', 'Woudenberg', 'IJsselstein',
    'Zeist']
deel_provincie_utrecht = ['De Bilt', 'Houten', 'Nieuwegein', 'Utrecht', 'Zeist']
features = ['aantal_inwoners', 'koopwoning_percentage', 'gemiddelde_woningwaarde', 
                         'leefbarometer_score', 'social_economische_score_gemiddeld']
analyse_gebied = deel_provincie_utrecht  #or use provincie_utrecht_gemeente
aantal_voorspellingen = 3

# prediction call api 
def get_prediction(analyse_gebied, buurt, features, aantal_voorspellingen):
    # url = "http://0.0.0.0:8000/predict" #local testing
    url = "http://fastapp:8000/predict"
    data = {
            "analyse_gebied": analyse_gebied,
            "buurt": buurt,
            "features": features,
            "aantal_voorspellingen": aantal_voorspellingen           
        }

    response = requests.post(url, json=data)
    # st.text(f'check health response:{response}')
    return response.text

# actual streamlit code
st.title('Buurten Vergelijker')
buurt = st.selectbox('Selecteer hieronder je favo-buurt: ',
    ('<select>', 'Oud Hoograven-Zuid', 'Voordorp en Voorveldsepolder', 'Slagen', 'Oorden', 'Poorten'))  

if buurt != '<select>':
    with st.spinner('Even wachten, de kaart wordt geladen...'):
        response = get_prediction(analyse_gebied, buurt, features, aantal_voorspellingen)
        html_map = BeautifulSoup(response, "html.parser") 

        with open('output.html', 'w', encoding='utf-8') as file:
            file.write(html_map.prettify())        

        with open('output.html', 'r') as f:
            html_map = f.read()

        if html_map:
            st.markdown('Viola, de volgende 3 buurten lijken op jouw favoriet: ')
            components.html(html_map, height=600, width=700)
else:
    st.markdown('Wat is jouw favoriete buurt? Selecteer je buurt en de vergelijker doet zijn werk...')
    # st.image(image=img, caption="Buurten Vergelijker") 