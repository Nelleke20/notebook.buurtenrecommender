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

# flexible dropping list
drop_buurten_houten = ['Buitengebied Houten West', 'Buitengebied Houten Oost', "Dorp 't Goy", "'t Goyse Dorp",
        "Buitengebied 't Goy", "'t Waal", 'Tull', "Buitengebied Tull en 't Waal", 'Dorp Schalkwijk West', 'Dorp Schalkwijk Oost', 'Buitengebied Schalkwijk West',
        'Buitengebied Schalkwijk Oost','Bruggen', 'Bogen', 'De Poel', 'Schepen', 'Boten', 'Honen', 'Kaden', 'Vesten', 'De Staart',
        'Hof van Wulven', 'Rondweg Noord-Oost', 'Rondweg Noord-West', 'Rondweg Zuid-Oost', 'Rondweg Zuid-West', 'Bedrijventerrein Lageweide',
        'Haarzuilens en omgeving', 'Bedrijventerrein en omgeving', 'Utrecht Science Park', 'Bedrijvengebied Strijkviertel', 'Bedrijvengebied Papendorp','Rijnenburg', 'Poldergebied Overvecht']


@dataclass
class CreateMap():
    file_path: str
    feature_column: str
    feature_selection: List
    feature_map_drop: str
    drop_buurten_map: List

    def _initialize_map(self):
        map = read_dataframe(self.file_path)        # lot faster processing
        # map = gpd.read_file(self.file_path, predicate="within")
        return map

    def _sub_map_selection(self, map):
        sub_map = map.loc[map[self.feature_column].isin(self.feature_selection)]
        return sub_map

    def _clean_up_columns(self, map):
        clean_map = map.loc[~map[self.feature_map_drop].isin(self.drop_buurten_map)]
        return clean_map

    def create_map(self, clean_up):
        map = self._initialize_map()
        sub_map = self._sub_map_selection(map)
        if clean_up:
            sub_map = self._clean_up_columns(sub_map)
        return sub_map

@dataclass
class CosineRecommender():
    input_features: str
    buurt_id: str
    buurten: str
    gem_map: str

    def _create_cosine_matrix(self):
        cosine_sim_matrix = cosine_similarity(self.input_features, self.input_features)
        return cosine_sim_matrix

    def _get_highest_scores(self, code_van_buurt, cosine_sim_matrix, n_predictions):

        # get all buurt-codes in de dataset en de indices die daarbij horen
        # buurten_code = self.buurten['buurt_code']
        indice_per_buurtcode = pd.Series(self.buurten.index, index=self.buurten['buurt_code'])

        # create dataframe with predictions
        indice_voor_selected_buurtcode = indice_per_buurtcode[code_van_buurt]

        # get score voor sim_score
        sim_scores_per_andere_buurt = list(enumerate(cosine_sim_matrix[indice_voor_selected_buurtcode]))
        sim_scores_per_andere_buurt = sorted(sim_scores_per_andere_buurt, key=lambda x: x[1], reverse=True)
        sim_scores_top_n = sim_scores_per_andere_buurt[1:n_predictions+1]  # without own similarity

        # get scores as seperate list
        scores = [i[1] for i in sim_scores_top_n]
        scores = [round(score, 4) for score in scores]
        
        # get names of the buurten that are recommended
        buurten_indices = [i[0] for i in sim_scores_top_n]
        return buurten_indices, scores

    def _create_recommendation(self, input_buurt, n_predictions):

        # zet naam om naar id van de buurt
        code_van_buurt = self.buurt_id.loc[self.buurt_id['regio'] == input_buurt, 'buurt_code'].item()

        # create matrix
        cosine_sim_matrix = self._create_cosine_matrix()

        # get indices and scores
        buurten_indices, scores = self._get_highest_scores(code_van_buurt, cosine_sim_matrix, n_predictions)

        # generate recommendations
        recommendations = self.buurten.iloc[buurten_indices]['buurt_code'].to_list()
        recommendations_df = pd.DataFrame(list(zip(recommendations, scores)))
        recommendations_naam = self.buurt_id.loc[self.buurt_id['buurt_code'].isin(recommendations), 'regio'].to_list()

        return recommendations_df, recommendations_naam, code_van_buurt, recommendations


    def list_and_plot_generator(self, input_buurt, n_predictions):

        # recommendations
        recommendations_df, recommendations_naam, code_van_buurt, recommendations = self._create_recommendation(input_buurt, n_predictions)

        # create plot with predictions

        merged_df = self.gem_map.merge(recommendations_df, left_on='BU_CODE', right_on=0, how='left')
        merged_df.loc[~merged_df[1].isnull(),'dummy'] = 1                       # green
        merged_df.loc[merged_df[1].isnull(),'dummy'] = 0.5                      # yellow
        merged_df.loc[merged_df['BU_NAAM'] == input_buurt, 'dummy'] = 0         # red

        # Maak een thematische kaart
        # fig, ax = plt.subplots() 
        ax = merged_df.plot(column="dummy",
                            figsize = (6,4),
                            cmap='RdYlGn')
        ax.axis('off')
        ax.set_title(f'Voor jouw buurt "{input_buurt}", \n adviseren we {recommendations_naam}.')  #
        plt.savefig('output_recommendations_top_n.png')     
        return 'De volgende buurten zijn aan te raden:', recommendations_naam, code_van_buurt, recommendations


@dataclass
class ExploreRecommender():
    gem_map: str
    buurten: str
    buurt_id: str
    recommendations: str
    code_van_buurt: str

    def explore_visualizer(self, features_visualisatie):

        geometry = self.gem_map[['geometry', 'BU_CODE']]
        geometry = geometry.merge(self.buurt_id, left_on='BU_CODE', right_on='buurt_code')
        explore = geometry.merge(self.buurten, left_on='BU_CODE', right_on='buurt_code', how='left')
        recommendations_plus_buurt = self.recommendations 
        recommendations_plus_buurt.append(self.code_van_buurt)

        explore = explore.loc[explore['BU_CODE'].isin(recommendations_plus_buurt)]
        explore = explore[explore.columns[explore.columns.isin(features_visualisatie)]]
        explore_interaction = explore.explore()

        return explore_interaction



def get_prediction(analyse_gebied, buurt, features, aantal_voorspellingen):

    buurten_path = Path(__file__).parent / "dataexception/buurten.csv"
    file_path_map = 'dataexception/map/buurt_2020_v3.shp'
    buurten = pd.read_csv(buurten_path, index_col=0)
    gemeente_selectie = [analyse_gebied]  
    buurt_voor_selectie = buurt
    n_predictions = aantal_voorspellingen
    features_visualisatie = features.extend(['geometry', 'regio', 'buurt_code'])

    ## run main
    map = CreateMap(file_path =file_path_map, 
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