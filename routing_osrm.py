import requests
from typing import Union
import polyline
import folium
import numpy as np

def route(coordinates , alternatives : Union[int,str] ="false", steps=False, annotations="false", geometries="polyline", overview="simplified"):
    """
    Parameters
    ----------
    coordinates : List
        A list of coordinations that specifies origin and destination of the route. It can be more than 2 points.
    
    alternatives : "false" (default), "true", int
        Search for alternative routes. Passing a number alternatives=n searches for up to n alternative routes. Even if alternative routes are requested, a result cannot be guaranteed.
    
    steps: False (default), True
        Returned route steps for each route leg
    
    annotations : "false" (default), "true", "nodes", "distance", "duration", "datasources", "weight", "speed"
        Returns additional metadata for each coordinate along the route geometry.
    
    geometries : "polyline" (default), "polyline6", "geojson"
        Returned route geometry format (influences overview and per step).
    
    overview : "simplified" (default), "full", "false"
        Add overview geometry either full, simplified according to highest zoom level it could be display on, or not at all.

    Returns
    -------
    result[0] : dict
        A dictionary which is a transformed version of the response that contains route(s) values
    result[1] : json
        Full response of the request as a json file
    
    """
    ## EXTRACT ##

        ## Checking parameters of the request
    alternatives_url = steps_url = geometries_url = annotations_url = overview_url = ""

    if alternatives == "false":
        pass
    else:
        alternatives_url = f"&alternatives={str(alternatives)}"
    
    if steps:
        steps_url = f"&steps=true"
    
    geometries_url = f"?geometries={geometries}"

    if annotations == "false":
        pass
    else:
        annotations_url = f"&annotations={annotations}"

    if overview == "simplified":
        pass
    else:
        overview_url = f"&overview={overview}"

    if len(coordinates) >= 2 :
        coordinates_url = ""
        for coordinate in coordinates:
            coordinates_url += f"{coordinate[1]},{coordinate[0]};"
        coordinates_url = coordinates_url[:-1]
    else:
        return "Error: less than 2 coordinates has been given"

        ## Creating request
    osrm_url = "http://router.project-osrm.org/route/v1/driving/"
    request_url = f"{osrm_url}{coordinates_url}{geometries_url}{alternatives_url}{steps_url}{annotations_url}{overview_url}"
    response = requests.get(request_url)
    print(request_url)

    if response.status_code != 200:
        return "Error: The response status code is not 200"
    
    response = response.json()

    ## TRANSFORM ##

    routes = {'start_point_latitude': [],
              'start_point_longitude': [],
              'end_point_latitude': [],
              'end_point_longitude': [],
              'route_number': [],
              'geometry': [],
              'route_coordinates': [],
              'distance': [],
              'duration': []}
    
    i = 0
    while i < len(response):

        routes['start_point_latitude'].append(coordinates[0][0])
        routes['start_point_longitude'].append(coordinates[0][1])
        routes['end_point_latitude'].append(coordinates[-1][0])
        routes['end_point_longitude'].append(coordinates[-1][1])
        routes['route_number'].append(i+1)
        if geometries == 'geojson':
            routes['geometry'].append(np.nan)
            routes['route_coordinates'].append(response['routes'][i]['geometry']['coordinates'])
        elif geometries == 'polyline6':
            routes['geometry'].append(response['routes'][i]['geometry'])
            routes['route_coordinates'].append(np.nan)
        else:
            routes['geometry'].append(response['routes'][i]['geometry'])
            routes['route_coordinates'].append(polyline.decode(response['routes'][i]['geometry']))
        routes['distance'].append(response['routes'][i]['distance'])
        routes['duration'].append(response['routes'][i]['duration'])

        i += 1

    return routes, response