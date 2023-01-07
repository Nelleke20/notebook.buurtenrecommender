import src.buurten as br
import pandas as pd
import matplotlib.pyplot as plt
import ssl
import geopandas as gpd
ssl._create_default_https_context = ssl._create_unverified_context
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import webbrowser
import os


# settings
file_path_map = 'data/buurt_2020_v3.shp'
file_path_buurten = 'data/buurten.csv'
gemeente_selectie = ['Houten', 'Utrecht']
clean_up = True
buurt_voor_selectie = 'Poorten'
n_predictions = 5
features_visualisatie = ['geometry', 'regio', 'buurt_code',  'aantal_inwoners',  'aantal_inwoners_tussen_25_44_percentage', 
'gemiddelde_huishoudensgrootte', 'woningvoorraad',  'gemiddelde_woningwaarde',  'meergezinswoning_percentage', 
'bewoond_percentage', 'koopwoning_percentage', 'bouwjaar_vanaf_2000_percentage', 'afstand_tot_grote_supermarkt_km', 
'afstand_tot_park_of_plantsoen_km', 'afstand_tot_hoofdverkeersweg_km', 'afstand_tot_treinstation_km', 'leefbarometer_score', 
'aardgasverbruik_m3_gemiddeld', 'elektriciteitsverbruik_kwh_gemiddeld', 'social_economische_score_gemiddeld', 'geluid_van_treinverkeer',
'geluid_van_weg']



## run main
drop_buurten_houten = ['Buitengebied Houten West', 'Buitengebied Houten Oost', "Dorp 't Goy", "'t Goyse Dorp",
        "Buitengebied 't Goy", "'t Waal", 'Tull', "Buitengebied Tull en 't Waal", 'Dorp Schalkwijk West', 'Dorp Schalkwijk Oost', 'Buitengebied Schalkwijk West',
        'Buitengebied Schalkwijk Oost','Bruggen', 'Bogen', 'De Poel', 'Schepen', 'Boten', 'Honen', 'Kaden', 'Vesten', 'De Staart',
        'Hof van Wulven', 'Rondweg Noord-Oost', 'Rondweg Noord-West', 'Rondweg Zuid-Oost', 'Rondweg Zuid-West', 'Bedrijventerrein Lageweide',
        'Haarzuilens en omgeving', 'Bedrijventerrein en omgeving', 'Utrecht Science Park', 'Bedrijvengebied Strijkviertel', 'Bedrijvengebied Papendorp','Rijnenburg', 'Poldergebied Overvecht']


map = br.CreateMap(file_path =file_path_map, 
                feature_column ='GM_NAAM', 
                feature_selection=gemeente_selectie, 
                feature_map_drop = 'BU_NAAM',
                drop_buurten_map=drop_buurten_houten)
gem_map = map.create_map(clean_up=clean_up) 

buurten = pd.read_csv(file_path_buurten, index_col=0)
buurten = buurten.loc[buurten['gm_naam'].isin(gemeente_selectie)]
buurten = buurten.reset_index(drop=True)
buurten = buurten.dropna()  #for now we just drop them
buurt_id = buurten[['buurt_code', 'regio']]
buurten = buurten.drop(['gm_naam', 'regio'], axis=1)

y_id_buurten = pd.DataFrame(buurten['buurt_code'])
X = buurten[buurten.columns[~buurten.columns.isin(y_id_buurten.columns)]]

recommender = br.CosineRecommender(
        input_features = X,
        buurt_id= buurt_id,
        buurten= buurten,
        gem_map= gem_map
)

output, recommendations_naam, code_van_buurt, recommendations  = recommender.list_and_plot_generator(buurt_voor_selectie, n_predictions)

explore = br.ExploreRecommender(    
    gem_map = gem_map, 
    buurten = buurten,
    buurt_id = buurt_id,
    recommendations = recommendations,
    code_van_buurt = code_van_buurt
)

explore = explore.explore_visualizer(features_visualisatie)
explore.save('recommendations_map.html')
return webbrowser.open('file://' + os.path.realpath('recommendations_map.html'))