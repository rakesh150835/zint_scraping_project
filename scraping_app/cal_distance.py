import requests


access_token = "pk.eyJ1Ijoicms4MzUiLCJhIjoiY20xcWM5Y2djMGM4cjJqczZ2ZXg3MzdybiJ9.p6MfeqQv99QEYz8SBblmAA"  # Replace with your Mapbox token



def get_lat_long_from_postcode(postcode, access_token):
    try:
        url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{postcode}.json"
        
        params = {
            "access_token": access_token,
            "limit": 1  # Get only one result
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if response.status_code == 200 and data['features']:
            lon = data['features'][0]['center'][0]  # Longitude
            lat = data['features'][0]['center'][1]  # Latitude
            return lat, lon
        else:
            print(f"Error fetching coordinates for {postcode}: {response.status_code}, {data.get('message', '')}")
            return None
        
    except Exception as e:
        print("Error in get_lat_long_from_postcode: ", e)
        return None



def get_distance_from_mapbox(origin, destination, access_token):
    try:
        url = f"https://api.mapbox.com/directions/v5/mapbox/driving/{origin[1]},{origin[0]};{destination[1]},{destination[0]}"
        
        params = {
            "access_token": access_token,
            "geometries": "geojson"
        }

        # Make the request to Mapbox API
        response = requests.get(url, params=params)
        data = response.json()
        
        if response.status_code == 200 and data['routes']:
            # Get the distance (in meters) and duration (in seconds)
            distance_meters = data['routes'][0]['distance']
            duration_seconds = data['routes'][0]['duration']

            # Convert distance to kilometers and duration to minutes
            distance_km = distance_meters / 1000
            duration_min = duration_seconds / 60

            return distance_km, duration_min
        else:
            print(f"Error fetching data: {response.status_code}, {data.get('message', '')}")
            return None
        
    except Exception as e:
        print("Error in get_distance_from_mapbox: ", e)
        return None


# Example usage

def cal_distance(postcode_1, postcode_2):
    try:  # Replace with your Mapbox token
        postcode_1 = postcode_1  # Postcode for one location
        postcode_2 = postcode_2  # Postcode for another location

        coords_1 = get_lat_long_from_postcode(postcode_1, access_token)
        coords_2 = get_lat_long_from_postcode(postcode_2, access_token)

        # calculate distance between two postcodes
        if coords_1 and coords_2:
            distance, duration = get_distance_from_mapbox(coords_1, coords_2, access_token)
            if distance:
                return distance
            else:       
                return None
        else:
            return None
        
    except Exception as e:
        print("Error in cal_distance: ", e)
        return None
        