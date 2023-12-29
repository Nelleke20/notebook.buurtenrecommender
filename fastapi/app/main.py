from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import utils as utils
import pandas as pd
from fastapi.responses import HTMLResponse

# flexible dropping list
drop_buurten_houten = ['Buitengebied Houten West', 'Buitengebied Houten Oost', "Dorp 't Goy", "'t Goyse Dorp",
        "Buitengebied 't Goy", "'t Waal", 'Tull', "Buitengebied Tull en 't Waal", 'Dorp Schalkwijk West', 'Dorp Schalkwijk Oost', 'Buitengebied Schalkwijk West',
        'Buitengebied Schalkwijk Oost','Bruggen', 'Bogen', 'De Poel', 'Schepen', 'Boten', 'Honen', 'Kaden', 'Vesten', 'De Staart',
        'Hof van Wulven', 'Rondweg Noord-Oost', 'Rondweg Noord-West', 'Rondweg Zuid-Oost', 'Rondweg Zuid-West', 'Bedrijventerrein Lageweide',
        'Haarzuilens en omgeving', 'Bedrijventerrein en omgeving', 'Utrecht Science Park', 'Bedrijvengebied Strijkviertel', 'Bedrijvengebied Papendorp','Rijnenburg', 'Poldergebied Overvecht']

# create app
app = FastAPI()

class Data(BaseModel):
    analyse_gebied: list
    buurt: str
    features: list
    aantal_voorspellingen: int

# home
@app.get("/")
def main():
    return {"message": "test-message"}

# defining prediction endpoint
@app.post("/predict", response_class=HTMLResponse)
def predict(data: Data):
    #settings
    file_path_map = 'map/buurt_2020_v3.shp'
    buurten = pd.read_csv('buurten.csv', index_col=0)  
    gemeente_selectie = data.analyse_gebied  
    buurt_voor_selectie = data.buurt
    n_predictions = data.aantal_voorspellingen
    features_visualisatie = data.features.extend(['geometry', 'regio', 'buurt_code'])

    ## run main
    map = utils.CreateMap(file_path =file_path_map, 
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

    recommender = utils.CosineRecommender(
            input_features = X_input,
            buurt_id= buurt_id,
            buurten= buurten,
            gem_map= gem_map
    )
    recommendations_naam, code_van_buurt, recommendations, = recommender.list_and_plot_generator(buurt_voor_selectie, n_predictions)

    explore = utils.ExploreRecommender(    
        gem_map = gem_map, 
        buurten = buurten,
        buurt_id = buurt_id,
        recommendations = recommendations,
        code_van_buurt = code_van_buurt
    )
    explore = explore.explore_visualizer(data.features)
    map_html = explore._repr_html_()
    return map_html  #html as str, later transform

if __name__ == "__main__":
    uvicorn.run(app)