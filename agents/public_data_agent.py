# agents/public_data_agent.py

import pandas as pd
import requests
import plotly.express as px

from utils.geo import geocode_location

def fetch_public_data(lugar: str, tipo_dato: str, periodo: int):
    """
    Consulta datos públicos para 'lugar' y 'tipo_dato'. 
    Si tipo_dato == "Riesgos de Inundación", descarga un GeoJSON de inundaciones 
    (publicado en GitHub u otra fuente) y genera un mapa PyDeck.
    Si es Demográficos, Meteorológicos, Sísmicos o Económicos, genera datos simulados.
    Retorna:
      - df: DataFrame con columnas ['fecha', 'valor'] o (en inundación) DataFrame vacío.
      - fig: Plotly Figure (línea/barra) o (en inundación) un dict con 'geojson' y 'view_state'.
      - geo_info: resultados de geocoding (lat, lon, display_name).
    """

    # 1) Geocodificar la ubicación
    geo_info = geocode_location(lugar)
    lat = geo_info.get("lat")
    lon = geo_info.get("lon")

    df = pd.DataFrame()
    fig = {}

    # Si no hay coords, devolvemos ya sin error
    if lat is None or lon is None:
        return {"df": df, "fig": fig, "geo_info": geo_info}

    # 2) Según tipo_dato
    if tipo_dato == "Demográficos":
        # Simulación de población total por año
        try:
            years = list(range(2025 - periodo, 2026))
            valores = [1_000_000 + i * 50_000 for i in range(len(years))]
            df = pd.DataFrame({"fecha": years, "valor": valores})
            df["fecha"] = pd.to_datetime(df["fecha"], format="%Y")
            fig = px.line(
                df,
                x="fecha",
                y="valor",
                title=f"Población estimada en {lugar} ({2025 - periodo}–2025)"
            )
            fig.update_layout(xaxis_title="Año", yaxis_title="Población", template="plotly_white")
        except Exception:
            df = pd.DataFrame()
            fig = {}

    elif tipo_dato == "Meteorológicos":
        # Simulación de temperatura promedio anual
        try:
            years = list(range(2025 - periodo, 2026))
            temps = [20 + i * 0.2 for i in range(len(years))]
            df = pd.DataFrame({"fecha": years, "valor": temps})
            df["fecha"] = pd.to_datetime(df["fecha"], format="%Y")
            fig = px.line(
                df,
                x="fecha",
                y="valor",
                title=f"Temperatura promedio anual en {lugar} ({2025 - periodo}–2025)"
            )
            fig.update_layout(xaxis_title="Año", yaxis_title="Temperatura (°C)", template="plotly_white")
        except Exception:
            df = pd.DataFrame()
            fig = {}

    elif tipo_dato == "Sísmicos":
        # Simulación de número de sismos anuales
        try:
            years = list(range(2025 - periodo, 2026))
            sismos = [5 + i for i in range(len(years))]
            df = pd.DataFrame({"fecha": years, "valor": sismos})
            df["fecha"] = pd.to_datetime(df["fecha"], format="%Y")
            fig = px.bar(
                df,
                x="fecha",
                y="valor",
                title=f"Número de sismos en {lugar} ({2025 - periodo}–2025)"
            )
            fig.update_layout(xaxis_title="Año", yaxis_title="Número de sismos", template="plotly_white")
        except Exception:
            df = pd.DataFrame()
            fig = {}

    elif tipo_dato == "Económicos":
        # Simulación de ingreso per cápita
        try:
            years = list(range(2025 - periodo, 2026))
            ingresos = [20_000 + i * 1_000 for i in range(len(years))]
            df = pd.DataFrame({"fecha": years, "valor": ingresos})
            df["fecha"] = pd.to_datetime(df["fecha"], format="%Y")
            fig = px.line(
                df,
                x="fecha",
                y="valor",
                title=f"Ingreso per cápita en {lugar} ({2025 - periodo}–2025)"
            )
            fig.update_layout(xaxis_title="Año", yaxis_title="Ingreso per cápita (MXN)", template="plotly_white")
        except Exception:
            df = pd.DataFrame()
            fig = {}

    elif tipo_dato == "Riesgos de Inundación":
        # Aquí descargamos un GeoJSON público de inundaciones (ejemplo de USGS/GitHub)
        # Para producción, reemplaza con un GeoJSON oficial de CONAGUA o INEGI.
        try:
            # Ejemplo genérico: GeoJSON de zonas inundables de EE.UU. (solo de demo)
            geojson_url = "https://raw.githubusercontent.com/giswqs/planetscope-analyses/master/data/us-flood-zones.geojson"
            resp = requests.get(geojson_url, timeout=15)
            if resp.status_code == 200 and resp.text.strip() != "":
                flood_geojson = resp.json()
                # Preparar un layer de PyDeck (ver main.py más abajo)
                fig = {
                    "geojson": flood_geojson,
                    "view_state": {
                        "latitude": lat,
                        "longitude": lon,
                        "zoom": 10,
                        "pitch": 0
                    }
                }
                df = pd.DataFrame()  # No devolvemos tabla numérica aquí
            else:
                df = pd.DataFrame()
                fig = {}
        except Exception:
            df = pd.DataFrame()
            fig = {}

    else:
        # Cualquier otro tipo o si no coincide, devolvemos vacíos
        df = pd.DataFrame()
        fig = {}

    return {
        "df": df,
        "fig": fig,
        "geo_info": geo_info
    }
