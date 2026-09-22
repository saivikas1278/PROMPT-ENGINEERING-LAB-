import os
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def geocode_location(location_name, api_key):
    url = f"https://graphhopper.com/api/1/geocode?q={location_name}&key={api_key}&limit=1"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data.get("hits"):
            point = data["hits"][0]["point"]
            return point["lat"], point["lng"]
    except requests.exceptions.RequestException as e:
        logger.error(f"Geocoding error for {location_name}: {e}")
    return None, None

def get_graphhopper_route(source, destination):
    """
    Fetches road route from GraphHopper API.
    Returns distance, travel_time, and path (if available), None otherwise.
    """
    api_key = os.getenv("GRAPHHOPPER_API_KEY")
    if not api_key:
        logger.error("GRAPHHOPPER_API_KEY environment variable not found.")
        return None

    # Geocode locations
    src_lat, src_lng = geocode_location(source, api_key)
    dst_lat, dst_lng = geocode_location(destination, api_key)

    if not src_lat or not dst_lat:
        logger.warning(f"Could not geocode {source} or {destination}")
        return None

    url = f"https://graphhopper.com/api/1/route?point={src_lat},{src_lng}&point={dst_lat},{dst_lng}&vehicle=car&key={api_key}&points_encoded=false"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if "paths" not in data or not data["paths"]:
            logger.info("No routes found from GraphHopper API.")
            return None
            
        path = data["paths"][0]
        
        distance_km = round(path.get("distance", 0) / 1000.0, 1)
        travel_time_minutes = path.get("time", 0) // 60000
        
        return {
            "distance": distance_km,
            "travel_time": travel_time_minutes,
            "path": path.get("points") # Encoded polyline
        }
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error calling GraphHopper Routing API: {e}")
        return None
