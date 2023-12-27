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
from utils import CreateMap, CosineRecommender, ExploreRecommender, Predictor

# path settings
bp = Path(__file__).parent / "demodata/buurten.csv"
mp = Path(__file__).parent / "demodata/map/buurt_2020_v3.shp"

st.title('Buurten recommender')
buurt = st.selectbox('Welke buurt wil je analyseren?',
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
    st.markdown('geef in het dropdown menu aan welke buurt in de provincie Utrecht je wilt vergelijken')