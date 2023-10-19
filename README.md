# Steel_Value_Chain

This project is my first data engineering project. The goal is to get a view of steel value chain in Iran by following these steps:

## Data Gathering
The source of information is infosaba.com. Using web scrapping ([Saba_Scrapping](#saba-scrapping.py)), I gathered required data which is loaded into 4 tables.
- Industries: Main industries of Iran such as Steel, Gold, Cement, etc.
- Units: Production units of each industry. For Example in Steel industry we have iron concentrate, rebar, hot sheets, etc.
- Complexes: All complexes which are active in main industries.
- Unit_Complex: Information about Complexes and their production units.

## Data Transformation
geopy uses OpenStreetMaps services to decode locations.By giving it the name of the location, it returns lat-long coordinations of the location (if the name is equal to OpenStreetMaps equivalent name). With help of human supervision, coordinations of Complexes are gathered.

## Routing
Now that we have complexes and their coordinations, we want to be able to measure the distance and duration betweet production units of the steel value chain. Using [ORSM](#https://project-osrm.org/docs/v5.24.0/api/) API service, I developed a customized [routing script](#routing_osrm.py) as I need.

## Visualization
In the [project run file](#project_.ipynb), all steps of the project is done.
For an example of the use-case of the [routing script](#routing_osrm.py), I followed all steps above and generated a distance matrix for complexes that produce Colored Sheets and need source complexes that produce Galvanized Sheets. Then as an example for distance matrix, a visualization for possible routes from 'مجتمع فولاد مبارکه' to 'مجتمع هفت الماس' has been illustrated. 
