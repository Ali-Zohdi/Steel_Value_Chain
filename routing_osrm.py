import requests

def OSRM_routes(coords_1, coords_2):

    osrm_url = "http://router.project-osrm.org/route/v1/driving/"
    request_url = f"{osrm_url}{coords_1[1]},{coords_1[0]};{coords_2[1]},{coords_2[0]}"
    response = requests.get(request_url)

    if response.status_code == 200 :
        
        data = response.json()

        distance = data['routes'][0]['distance']
        print(f"The distance using OSRM is: {distance}")
    else:
        print("Response status code is not 200!")

