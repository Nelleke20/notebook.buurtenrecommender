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
from dataclasses import dataclass
from typing import List
import geopandas as gpd
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import matplotlib.pyplot as plt
from pyogrio import read_dataframe
from pathlib import Path
from utils import CreateMap, CosineRecommender, ExploreRecommender

# flexible dropping list
drop_buurten_houten = ['Buitengebied Houten West', 'Buitengebied Houten Oost', "Dorp 't Goy", "'t Goyse Dorp",
        "Buitengebied 't Goy", "'t Waal", 'Tull', "Buitengebied Tull en 't Waal", 'Dorp Schalkwijk West', 'Dorp Schalkwijk Oost', 'Buitengebied Schalkwijk West',
        'Buitengebied Schalkwijk Oost','Bruggen', 'Bogen', 'De Poel', 'Schepen', 'Boten', 'Honen', 'Kaden', 'Vesten', 'De Staart',
        'Hof van Wulven', 'Rondweg Noord-Oost', 'Rondweg Noord-West', 'Rondweg Zuid-Oost', 'Rondweg Zuid-West', 'Bedrijventerrein Lageweide',
        'Haarzuilens en omgeving', 'Bedrijventerrein en omgeving', 'Utrecht Science Park', 'Bedrijvengebied Strijkviertel', 'Bedrijvengebied Papendorp','Rijnenburg', 'Poldergebied Overvecht']


######################## MAIN SCRIPT ########################

def get_prediction(analyse_gebied, buurt, features, aantal_voorspellingen):

    buurten_path = Path(__file__).parent / "dataexception/buurten.csv"
    map_path = Path(__file__).parent / "dataexception/map/buurt_2020_v3.shp"
    buurten = pd.read_csv(buurten_path, index_col=0)
    gemeente_selectie = [analyse_gebied]  
    buurt_voor_selectie = buurt
    n_predictions = aantal_voorspellingen
    features_visualisatie = features.extend(['geometry', 'regio', 'buurt_code'])

    ## run main
    map = CreateMap(file_path =map_path, 
                    feature_column ='GM_NAAM', 
                    feature_selection=gemeente_selectie, 
                    feature_map_drop = 'BU_NAAM',
                    drop_buurten_map=drop_buurten_houten)
    gem_map = map.create_map(clean_up=True) 

    buurten = buurten.loc[buurten['gm_naam'].isin(gemeente_selectie)]
    buurten = buurten.reset_index(drop=True)
    buurten = buurten.dropna()  # for now we just drop them
    buurt_id = buurten[['buurt_code', 'regio']]
    buurten = buurten.drop(['gm_naam', 'regio'], axis=1)

    y_id_buurten = pd.DataFrame(buurten['buurt_code'])
    X_input = buurten[buurten.columns[~buurten.columns.isin(y_id_buurten.columns)]]

    recommender = CosineRecommender(
            input_features = X_input,
            buurt_id= buurt_id,
            buurten= buurten,
            gem_map= gem_map
    )
    output, recommendations_naam, code_van_buurt, recommendations, = recommender.list_and_plot_generator(buurt_voor_selectie, n_predictions)

    explore = ExploreRecommender(    
        gem_map = gem_map, 
        buurten = buurten,
        buurt_id = buurt_id,
        recommendations = recommendations,
        code_van_buurt = code_van_buurt
    )
    explore = explore.explore_visualizer(features)
    map_html = explore._repr_html_()
    return map_html  #html as str, later transform


st.title('Buurten recommender')
input_values=''
with st.sidebar:
    analyse_gebied = st.selectbox('In welk gebied wil je je verdiepen?',
        ('Utrecht', 'Houten'))    
    if analyse_gebied:
        with st.form("my_form"):
            st.subheader('Definieer de settings voor de recommender hier:')
            
            if analyse_gebied == 'Utrecht':
                buurt = st.selectbox('Welke buurt wil je analyseren?',
                    ('Oud Hoograven-Zuid', 'Voordorp en Voorveldsepolder'))
            elif analyse_gebied == 'Houten':
                buurt = st.selectbox('Welke buurt wil je analyseren?',
                    ('Slagen', 'Oorden', 'Poorten'))        

            features = st.multiselect(
                "Kies max 5 features die je wilt visualiseren per buurt:",
                ["aantal_inwoners", "aantal_inwoners_tussen_25_44_percentage", "gemiddelde_huishoudensgrootte", "woningvoorraad"],
                max_selections=5,
            )

            aantal_voorspellingen = st.slider('Hoeveel buurten wil je als voorspelling terugkrijgen?', 0, 10, 1)

            submitted = st.form_submit_button("Run!")
            if submitted:
                input_values = [analyse_gebied, buurt, features, aantal_voorspellingen]
                print(input_values)

if input_values:
    with st.spinner('Nog even wachten, de kaart wordt geladen...'):
        response = get_prediction(analyse_gebied, buurt, features, aantal_voorspellingen)
        html_map = BeautifulSoup(response, "html.parser") 

        with open('output.html', 'w', encoding='utf-8') as file:
            file.write(html_map.prettify())        

        with open('output.html', 'r') as f:
            html_map = f.read()

        components.html(html_map, height=600, width=700)
else:
    st.markdown('geef in het menu links aan welke settings je wilt gebruiken om een analyse te doen')