### Introduction
Still trying to look for a house and somethimes we pass a very nice neighborhoud. So the question I tried to answer was, if we like specific buurt in our province; can we find others that are look a likes?  
This way creating a recommendersytem for buurten based on specific demographics of the place.

#### Starting date
Dec 1, 2022

#### Context
To be able to analyse what several aspects within 'buurten', I collected data from several sources:

Open CBS data: https://www.cbs.nl/nl-nl/achtergrond/2022/14/statusscore-per-wijk-en-buurt-o-b-v-welvaart-opleidingsniveau-en-arbeid

leefbarometer score: https://www.leefbaarometer.nl/tabel.php?indicator=Leefbaarheidssituatie&schaal=Buurt&gemeente=GM0344

geluidsblootstelling: https://statline.rivm.nl/portal.html?_la=nl&_catalog=RIVM&tableId=50066NED&_theme=96

woningvoorraad: https://opendata.cbs.nl/statline/#/CBS/nl/dataset/83704NED/table

tevredenheidscores: https://opendata.cbs.nl/statline/#/CBS/en/dataset/84571ENG/table

input features eventually used:

>    ['buurt_code', 'gm_naam', 'regio', 'aantal_inwoners','aantal_inwoners_tussen_25_44_percentage',
>    'aantal_huishoudens_met_kinderen_percentage', 'gemiddelde_huishoudensgrootte', 'woningvoorraad',
>    'gemiddelde_woningwaarde', 'meergezinswoning_percentage', 'bewoond_percentage', 'koopwoning_percentage',
>    'bouwjaar_vanaf_2000_percentage', 'afstand_tot_ziekenhuis_km', 'afstand_tot_grote_supermarkt_km', 'afstand_tot_cafe_km',
>    'afstand_tot_kinderdagverblijf_km', 'afstand_tot_buitenschoolseopvang_km', 'afstand_tot_openbaar_groen_km',
>    'afstand_tot_park_of_plantsoen_km', 'afstand_tot_bos_km','afstand_tot_hoofdverkeersweg_km', 'afstand_tot_treinstation_km',
>    'AfstandTotSemiOpenbaarGroenTotaal_83', 'leefbarometer_score', 'leefbarometer_fysieke_omgeving', 'leefbarometer_fysieke_overlast',
>    'leefbarometer_sociale_samenhang', 'leefbarometer_voorzieningen', 'aardgasverbruik_m3_gemiddeld', 
>    'elektriciteitsverbruik_kwh_gemiddeld', 'social_economische_score_gemiddeld', 'geluid_van_treinverkeer', 
>    'geluid_van_weg']

#### Results
to do: write up cosine similarity results

#### Application
Two options
1. demo streamlit app via their cloud: https://utrechtbuurten.streamlit.app/
2. Run or deploy docker app with fastapi backend and streamlit frontend (docker compose up).
   
#### Tech and Tools
recommender systemts, streamlit, fastapi