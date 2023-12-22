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
st.title('Buurten recommender')

file_path = '../notebooks/test.shp'
explore = gpd.read_file(file_path)

# Create a GeoDataFrame
gdf = gpd.GeoDataFrame(explore, geometry=explore['geometry'])

# Create a Folium map centered around the mean coordinates
center = [gdf.centroid.x.mean(), gdf.centroid.y.mean()]
center_dummy =[52.02721,5.17040]
m = folium.Map(location=center_dummy, zoom_start=13)

# # Add GeoJSON data to the map 
# for _, row in gdf.iterrows():
#     geojson_data = row['geometry'].__geo_interface__
#     print(geojson_data)  # Print GeoJSON data for each polygon
#     folium.GeoJson(geojson_data).add_to(m)

st_data = folium_static(m, width=725)