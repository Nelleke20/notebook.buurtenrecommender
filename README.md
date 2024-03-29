### Introduction
We sometimes pass very nice neigborhoods and imagined living there. At this point we are still trying to buy a house. When there are no houses available in these neigborhoods, we wished we would know other neigborhoods which are just as nice (and do have houses available). Therefore I decided to build an app which would recommend likeminded neigborhoods. Doesn't that sound very practical?

So the question I tried to answer was: If we like specific neigborhoods in our province, what are other neigborhoods that are lookalikes, based on features that we find important?  

#### Starting date
Dec 1, 2022

#### Context
To be able to analyse several aspects within 'buurten', I collected data from various sources:
* Open CBS data: [CBS buurt en wijk-dataset](https://www.cbs.nl/nl-nl/achtergrond/2022/14/statusscore-per-wijk-en-buurt-o-b-v-welvaart-opleidingsniveau-en-arbeid)
* Leefbarometer score:[Leefbarometer dataset](https://www.leefbaarometer.nl/tabel.php?indicator=Leefbaarheidssituatie&schaal=Buurt&gemeente=GM0344)
* Geluidsblootstelling: [RIVM geluidsoverlast-dataset](https://statline.rivm.nl/portal.html?_la=nl&_catalog=RIVM&tableId=50066NED&_theme=96)
* Woningvoorraad: [CBS woningvoorraad-dataset](https://opendata.cbs.nl/statline/#/CBS/nl/dataset/83704NED/table)
* Tevredenheidscores: [CBS sociaalecomischescore-datset](https://opendata.cbs.nl/statline/#/CBS/en/dataset/84571ENG/table)

**Input features eventually used:**

As we have several features that we found important (and based on some EDA), I decided to use the following variables:
>    ['aantal_inwoners', 'aantal_inwoners_tussen_25_44_percentage',
>    'aantal_huishoudens_met_kinderen_percentage', 'gemiddelde_huishoudensgrootte', 'woningvoorraad',
>    'gemiddelde_woningwaarde', 'meergezinswoning_percentage', 'bewoond_percentage', 'koopwoning_percentage',
>    'bouwjaar_vanaf_2000_percentage', 'afstand_tot_ziekenhuis_km', 'afstand_tot_grote_supermarkt_km', 'afstand_tot_cafe_km',
>    'afstand_tot_kinderdagverblijf_km', 'afstand_tot_buitenschoolseopvang_km', 'afstand_tot_openbaar_groen_km',
>    'afstand_tot_park_of_plantsoen_km', 'afstand_tot_bos_km','afstand_tot_hoofdverkeersweg_km', 'afstand_tot_treinstation_km',
>    'leefbarometer_score', 'leefbarometer_fysieke_omgeving', 'leefbarometer_fysieke_overlast',
>    'leefbarometer_sociale_samenhang', 'leefbarometer_voorzieningen', 'aardgasverbruik_m3_gemiddeld', 
>    'elektriciteitsverbruik_kwh_gemiddeld', 'social_economische_score_gemiddeld', 'geluid_van_treinverkeer', 
>    'geluid_van_weg']

#### Results
For each buurt we recommend 3 neighborhoods that are look-a-likes (determined by the cosine similarity score) based on the input variables above:

<p align="center" width="100%">
    <img width="75%" src="img/buurtrecommender.png">
</p>

To visualize relevant info, I decided to select 5 variables that are demonstrated per buurt.
However,do note that the analysis is done on all the variables and not just these 5.

#### Application
Two options:
1. Demo folder for streamlit app via their cloud: https://buurten.streamlit.app/
2. Run or deploy docker app with Fastapi backend and Streamlit frontend (docker compose up).

#### Tech and Tools
Recommendersystems, Streamlit (cloud), Fastapi