import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from dataclasses import dataclass
from typing import List
import geopandas as gpd
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import matplotlib.pyplot as plt
from pyogrio import read_dataframe
from pathlib import Path


# settings
provincie_utrecht_gemeente =['Amersfoort','Baarn', 'Bunnik', 'Bunschoten', 'De Bilt',
    'De Ronde Venen','Eemnes','Houten', 'Leusden', 'Lopik', 'Montfoort', 'Nieuwegein',
    'Oudewater','Renswoude', 'Rhenen', 'Soest', 'Stichtse Vecht', 'Utrecht', 'Utrechtse Heuvelrug',
    'Veenendaal', 'Vijfheerenlanden', 'Wijk bij Duurstede', 'Woerden', 'Woudenberg', 'IJsselstein',
    'Zeist']
deel_provincie_utrecht = ['De Bilt', 'Houten', 'Nieuwegein', 'Utrecht', 'Zeist']
visualisatie_features = ['aantal_inwoners', 'koopwoning_percentage', 'gemiddelde_woningwaarde', 
                         'leefbarometer_score', 'social_economische_score_gemiddeld']

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
        # get all buurt-codes and create dataframe
        indice_per_buurtcode = pd.Series(self.buurten.index, index=self.buurten['buurt_code'])
        indice_voor_selected_buurtcode = indice_per_buurtcode[code_van_buurt]

        sim_scores_per_andere_buurt = list(enumerate(cosine_sim_matrix[indice_voor_selected_buurtcode]))
        sim_scores_per_andere_buurt = sorted(sim_scores_per_andere_buurt, key=lambda x: x[1], reverse=True)
        sim_scores_top_n = sim_scores_per_andere_buurt[1:n_predictions+1]  # without own similarity

        scores = [i[1] for i in sim_scores_top_n]
        scores = [round(score, 4) for score in scores]
        buurten_indices = [i[0] for i in sim_scores_top_n]       
        return buurten_indices, scores

    def _create_recommendation(self, input_buurt, n_predictions):
        code_van_buurt = self.buurt_id.loc[self.buurt_id['regio'] == input_buurt, 'buurt_code'].item()
        cosine_sim_matrix = self._create_cosine_matrix() # create matrix
        buurten_indices, scores = self._get_highest_scores(code_van_buurt, cosine_sim_matrix, n_predictions)
        # generate recommendations
        recommendations = self.buurten.iloc[buurten_indices]['buurt_code'].to_list()
        recommendations_df = pd.DataFrame(list(zip(recommendations, scores)))
        recommendations_naam = self.buurt_id.loc[self.buurt_id['buurt_code'].isin(recommendations), 'regio'].to_list()
        return recommendations_df, recommendations_naam, code_van_buurt, recommendations


    def list_and_plot_generator(self, input_buurt, n_predictions, plot = False):
        recommendations_df, recommendations_naam, code_van_buurt, recommendations = self._create_recommendation(input_buurt, n_predictions)
        if plot:
            merged_df = self.gem_map.merge(recommendations_df, left_on='BU_CODE', right_on=0, how='left')
            merged_df.loc[~merged_df[1].isnull(),'dummy'] = 1                       # green
            merged_df.loc[merged_df[1].isnull(),'dummy'] = 0.5                      # yellow
            merged_df.loc[merged_df['BU_NAAM'] == input_buurt, 'dummy'] = 0         # red

            fig, ax = plt.subplots() 
            ax = merged_df.plot(column="dummy",
                                figsize = (6,4),
                                cmap='RdYlGn')
            ax.axis('off')
            ax.set_title(f'Voor jouw buurt "{input_buurt}", \n adviseren we {recommendations_naam}.')  #
            plt.savefig('output_recommendations_top_n.png')   
        else:
            print('not returning a plot')
        return recommendations_naam, code_van_buurt, recommendations


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
        # recommendations_plus_buurt.append(self.code_van_buurt)    #possible visualize buurt

        explore = explore.loc[explore['BU_CODE'].isin(recommendations_plus_buurt)]
        explore = explore[explore.columns[explore.columns.isin(features_visualisatie)]]   
        explore = explore.rename(columns={"regio": "Regio",
                                          "aantal_inwoners": "Inwoners (#)", 
                                          "koopwoning_percentage": "Koopwoningen (%)",
                                          "gemiddelde_woningwaarde": "Woningwaarde (gem)",
                                          "leefbarometer_score": "Leefbarometer (score)",
                                          "social_economische_score_gemiddeld": "SociaalEconomischeScore (gem)"})
        explore_interaction = explore.explore()
        return explore_interaction
    

@dataclass
class Predictor():
    buurten_path: str
    map_path: str

    def get_prediction(self, buurt):
        buurten = pd.read_csv(self.buurten_path, index_col=0)
        # gemeente_selectie = provincie_utrecht_gemeente 
        gemeente_selectie = deel_provincie_utrecht  # bit more concise
        buurt_voor_selectie = buurt
        features_visualisatie = visualisatie_features.extend(['geometry', 'regio', 'buurt_code'])

        ## run main
        map = CreateMap(file_path =self.map_path, 
                        feature_column ='GM_NAAM', 
                        feature_selection=gemeente_selectie, 
                        feature_map_drop = 'BU_NAAM',
                        drop_buurten_map=[])
        gem_map = map.create_map(clean_up=True) 

        buurten = buurten.loc[buurten['gm_naam'].isin(gemeente_selectie)]
        buurten = buurten.reset_index(drop=True)
        buurten = buurten.dropna()  # for now we just drop emtpy's 
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
        recommendations_naam, code_van_buurt, recommendations, = recommender.list_and_plot_generator(buurt_voor_selectie, n_predictions=3)

        explore = ExploreRecommender(    
            gem_map = gem_map, 
            buurten = buurten,
            buurt_id = buurt_id,
            recommendations = recommendations,
            code_van_buurt = code_van_buurt
        )
        explore = explore.explore_visualizer(visualisatie_features)
        map_html = explore._repr_html_()
        return map_html  #html as str, later transform