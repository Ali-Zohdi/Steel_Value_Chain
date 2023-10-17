import requests
from typing import Union

def route(coordinates , alternatives : Union[int,str] ="false", steps=False, annotations : Union[int,str] ="false", geometries="polyline", overview="simplified"):


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

    osrm_url = "http://router.project-osrm.org/route/v1/driving/"
    request_url = f"{osrm_url}{coordinates_url}{geometries_url}{alternatives_url}{steps_url}{annotations_url}{overview_url}"
    response = requests.get(request_url)
    print(request_url)

    if response.status_code == 200 :
        
        data = response.json()

        distance = data['routes'][0]['distance']
        print(f"The distance using OSRM is: {distance}")
    else:
        print("Response status code is not 200!")

    return data