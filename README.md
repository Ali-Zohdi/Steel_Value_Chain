# Steel_Value_Chain

This project is my first data engineering project. The goal is to get a view of the steel supply chain in Iran by following these steps:

## Data Gathering
The source of information is infosaba.com. Using web scraping ([Saba_Scrapping](#saba-scrapping.py)), I gathered the required data which was loaded into 4 tables.
- Industries: The main industries of Iran such as Steel, Gold, Cement, etc.
- Units: Production units of each industry. For example, in the Steel industry, we have iron concentrate, rebar, hot sheets, etc.
- Complexes: All complexes which are active in main industries.
- Unit_Complex: Information about Complexes and their production units.

## Data Transformation
geopy uses OpenStreetMaps services to decode locations. By giving it the name of the location, it returns lat-long coordinations of the location (if the name is equal to OpenStreetMaps equivalent name). With the help of human supervision, coordination of Complexes is gathered.

## Routing
Now that we have complexes and their coordinations, we want to be able to measure the distance and duration between production units of the steel value chain. Using [ORSM](#https://project-osrm.org/docs/v5.24.0/api/) API service, I developed a customized [routing script](#routing_osrm.py) as I needed.

## Visualization
In the [project run file](#project_.ipynb), all steps of the project are done.
For an example of the use-case of the [routing script](#routing_osrm.py), I followed all steps above and generated a distance matrix for complexes that produce Colored Sheets and need source complexes that produce Galvanized Sheets. Then as an example of distance matrix, a visualization for possible routes from 'مجتمع فولاد مبارکه' to 'مجتمع هفت الماس' has been illustrated.
