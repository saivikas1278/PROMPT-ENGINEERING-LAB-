import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def geocode_location(location_name):
    # Appending a generic context to improve geocoding for Indian cities, you can adjust this if needed.
    url = f"https://nominatim.openstreetmap.org/search?q={location_name}, India&format=json&limit=1"
    headers = {
        'User-Agent': 'PublicTransportAssistant/1.0 (saivikas1278)'
    }
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data and len(data) > 0:
            return float(data[0]["lat"]), float(data[0]["lon"])
    except requests.exceptions.RequestException as e:
        logger.error(f"Geocoding error for {location_name}: {e}")
    return None, None

def get_graphhopper_route(source, destination):
    """
    Fetches road route from OSRM public API (function kept same name for compatibility).
    Returns distance, travel_time, and path (if available), None otherwise.
    """
    # Geocode locations
    src_lat, src_lon = geocode_location(source)
    dst_lat, dst_lon = geocode_location(destination)

    if not src_lat or not dst_lat:
        logger.warning(f"Could not geocode {source} or {destination}")
        return None

    # OSRM expects longitude,latitude
    url = f"https://router.project-osrm.org/route/v1/driving/{src_lon},{src_lat};{dst_lon},{dst_lat}?overview=full&geometries=geojson"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if "routes" not in data or not data["routes"]:
            logger.info("No routes found from OSRM API.")
            return None
            
        route = data["routes"][0]
        
        distance_km = round(route.get("distance", 0) / 1000.0, 1)
        travel_time_minutes = int(route.get("duration", 0) // 60)
        
        return {
            "distance": distance_km,
            "travel_time": travel_time_minutes,
            "path": route.get("geometry") # GeoJSON geometry
        }
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error calling OSRM Routing API: {e}")
        return None
