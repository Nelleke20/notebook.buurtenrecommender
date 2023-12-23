import streamlit as st
import pandas as pd
import numpy as np
import buurten as br
import pandas as pd
import matplotlib.pyplot as plt
import ssl
from streamlit_folium import folium_static
import geopandas as gpd
ssl._create_default_https_context = ssl._create_unverified_context
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import webbrowser
import os
import folium
import streamlit.components.v1 as components

st.title('Buurten recommender')

with open('recommendations_map.html', 'r') as f:
    html_map = f.read()

components.html(html_map, height=600, width=700)

with st.sidebar:
    st.title('Set the input features here: ')
    st.slider('How many buurten to predict', 0, 10, 1)