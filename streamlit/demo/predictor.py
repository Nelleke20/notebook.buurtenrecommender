import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import pandas as pd
from pathlib import Path
from utils import CreateMap, CosineRecommender, ExploreRecommender


provincie_utrecht_gemeente =['Amersfoort','Baarn', 'Bunnik', 'Bunschoten', 'De Bilt',
    'De Ronde Venen','Eemnes','Houten', 'Leusden', 'Lopik', 'Montfoort', 'Nieuwegein',
    'Oudewater','Renswoude', 'Rhenen', 'Soest', 'Stichtse Vecht', 'Utrecht', 'Utrechtse Heuvelrug',
    'Veenendaal', 'Vijfheerenlanden', 'Wijk bij Duurstede', 'Woerden', 'Woudenberg', 'IJsselstein',
    'Zeist']

visualisatie_features = ['aantal_inwoners', 'koopwoning_percentage', 'gemiddelde_woningwaarde', 
                         'leefbarometer_score', 'social_economische_score_gemiddeld']


def get_prediction(buurt):
    buurten_path = Path(__file__).parent / "demodata/buurten.csv"
    map_path = Path(__file__).parent / "demodata/map/buurt_2020_v3.shp"
    buurten = pd.read_csv(buurten_path, index_col=0)
    gemeente_selectie = provincie_utrecht_gemeente 
    buurt_voor_selectie = buurt
    features_visualisatie = visualisatie_features.extend(['geometry', 'regio', 'buurt_code'])

    ## run main
    map = CreateMap(file_path =map_path, 
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
    output, recommendations_naam, code_van_buurt, recommendations, = recommender.list_and_plot_generator(buurt_voor_selectie, n_predictions=3)

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