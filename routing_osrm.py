import requests
from typing import Union
import polyline
import folium
import numpy as np
import pandas as pd

def route(coordinates , alternatives : Union[int,str] ="false", steps=False, annotations="false", geometries="polyline", overview="simplified"):
    """
    Finds the fastest route between coordinates in the supplied order.

    Parameters
    ----------
    coordinates : List
        A list of lat-long coordinations (lat, long) that specifies origin and destination of the route. It can be more than 2 points.
    
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
    result['routes'] : dict
        A dictionary which is a transformed version of the response that contains route(s) values
    result['response'] : json
        Full response of the request
    
    """
    #############
    ## EXTRACT ##
    #############

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
        return print("Error: less than 2 coordinates has been given")

        ## Creating request
    osrm_url = "http://router.project-osrm.org/route/v1/driving/"
    request_url = f"{osrm_url}{coordinates_url}{geometries_url}{alternatives_url}{steps_url}{annotations_url}{overview_url}"
    response = requests.get(request_url)

    if response.status_code != 200:
        return print(f"Error: The response status code is not 200 for {request_url}")
    
    response = response.json()

    ###############
    ## TRANSFORM ##
    ###############

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
    while i < len(response['routes']):

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

    result = {'routes': routes,
              'response': response}

    return result


def table(sources : list, sources_reference : list, destinations : list, destinations_reference : list):
    """
    Computes the duration of the fastest route between all pairs of supplied coordinates. Returns the durations or distances or both between the coordinate pairs. Note that the distances are not the shortest distance between two coordinates, but rather the distances of the fastest routes. Duration is in seconds and distances is in meters.

    Parameters
    ----------
    sources : list
        A list of lat-long coordinates (lat, long)
    
    sources_references : list
        A list of references like name or index for sources

    destinations : list
        A list of lat-long coordinates (lat, long)    

    destinations_references : list
        A list of references like name or index for destinations
    Return
    ------
    result['distance_m'] : DataFrame
        Distance table in Meters

    result['distance_km'] : DataFrame
        Distance table in Kiloeters
    
    result['duration_min'] : DataFrame
        Duration table in Minutes

    result['duration_h'] : DataFrame
        Duration table in Hours

    result['response'] : json
        Full response of the request
    """
    #############
    ## EXTRACT ##
    #############

        ## Checking parameters of the request
    annotations_url = "?annotations=distance,duration"

    if len(sources) == 0 or len(destinations) == 0:
        return print("Error: sources or destinations list is null")
    else:
        coordinates_url = ""
        sources_url = "&sources="
        destinations_url = "&destinations="
        
        i = 0
        while i < len(sources):
            coordinates_url += f"{sources[i][1]},{sources[i][0]};"
            sources_url += f"{i};"
            i += 1
        
        j = 0
        while j < len(destinations):
            coordinates_url += f"{destinations[j][1]},{destinations[j][0]};"
            destinations_url += f"{i+j};"
            j += 1

    coordinates_url = coordinates_url[:-1]
    sources_url = sources_url[:-1]
    destinations_url = destinations_url[:-1]

        ## Creating request
    osrm_url = "http://router.project-osrm.org/table/v1/driving/"
    request_url = f"{osrm_url}{coordinates_url}{annotations_url}{sources_url}{destinations_url}"
    response = requests.get(request_url)

    if response.status_code != 200:
        return print(f"Error: The response status code is not 200 for {request_url}")
    
    response = response.json()
            
    ###############
    ## TRANSFORM ##
    ###############

    distance_m = response['distances']
    duration_sec = response['durations']

    distance_km = [[x / 1000 for x in row] for row in distance_m]
    duration_min = [[x / 60 for x in row] for row in duration_sec]
    duration_h = [[x / 60 for x in row] for row in duration_min]

    distance_m = pd.DataFrame(distance_m, index=sources_reference, columns=destinations_reference)
    distance_km = pd.DataFrame(distance_km, index=sources_reference, columns=destinations_reference)
    duration_min = pd.DataFrame(duration_min, index=sources_reference, columns=destinations_reference)
    duration_h = pd.DataFrame(duration_h, index=sources_reference, columns=destinations_reference)

    result = {'distance_m': distance_m,
              'distance_km': distance_km,
              'duration_min': duration_min,
              'duration_h': duration_h,
              'response': response}

    return result

def get_map(route):
    
    m = folium.Map(location=[(route[0][0] + route[-1][0])/2, 
                             (route[0][1] + route[-1][1])/2],
                             zoom_start=7)

    folium.PolyLine(
        route,
        weight=8,
        color='blue',
        opacity=0.6
    ).add_to(m)

    folium.Marker(
        location=route[0],
        icon=folium.Icon(icon='play', color='green')
    ).add_to(m)

    folium.Marker(
        location=route[-1],
        icon=folium.Icon(icon='stop', color='red')
    ).add_to(m)

    return m