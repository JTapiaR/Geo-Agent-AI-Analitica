# utils/geo.py

import requests

def geocode_location(lugar: str) -> dict:
    """
    Usa Nominatim (OpenStreetMap) para geocodificar un texto de ubicación.
    Retorna diccionario con llaves:
      - lat  (float)
      - lon  (float)
      - display_name (str)
    Si no se encuentra nada o hay error, retorna {}.
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": lugar,
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "geoagentx/1.0 (tu_email@ejemplo.com)"
    }

    try:
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        if resp.status_code != 200 or resp.text.strip() == "":
            return {}
        data = resp.json()
        if not data:
            return {}

        item = data[0]
        lat = float(item.get("lat", 0))
        lon = float(item.get("lon", 0))
        display_name = item.get("display_name", "")
        return {"lat": lat, "lon": lon, "display_name": display_name}
    except (requests.RequestException, ValueError):
        return {}
