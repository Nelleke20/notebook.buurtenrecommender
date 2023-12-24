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
        # do api-call
        response = get_prediction(analyse_gebied, buurt, features, aantal_voorspellingen)
        html_map = BeautifulSoup(response, "html.parser") 

        with open('output.html', 'w', encoding='utf-8') as file:
            file.write(html_map.prettify())        

        with open('output.html', 'r') as f:
            html_map = f.read()

        components.html(html_map, height=600, width=700)
else:
    st.markdown('geef in het menu links aan welke settings je wilt gebruiken om een analyse te doen')