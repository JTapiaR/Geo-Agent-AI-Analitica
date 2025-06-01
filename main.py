## main.py

import os
import sys

import streamlit as st
import pandas as pd
import pydeck as pdk

# ─────────── Asegurar que la carpeta raíz esté en sys.path ───────────
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# Importar agentes
from agents.news_agent import fetch_and_process_news
from agents.user_data_agent import process_user_uploads
from agents.public_data_agent import fetch_public_data

# ─────────── Configuración de traducciones ───────────
TEXTS = {
    "es": {
        "app_title": "Geo-Agent-AI: Aplicación Multiagente de Datos Locales",
        "select_lang": "Selecciona idioma / Select language",
        "spanish": "Español",
        "english": "English",

        # Introducción
        "intro_header": "📄 Introducción a Geo-Agent-AI",
        "intro_text": (
            "Geo-Agent-AI es una **aplicación multiagente multimodal** diseñada para empoderar "
            "a comunidades y organizaciones a:\n\n"
            "1. **Buscar y procesar noticias** de un lugar específico.\n"
            "2. **Subir sus propios datos** (imágenes, audios, textos) asociados a una ubicación concreta.\n"
            "3. **Consultar datos oficiales y capas geoespaciales** (por ejemplo, riesgos de inundación) "
            "para contrastar la información.\n"
            "4. **Realizar un análisis combinado** de las tres fuentes (noticias, datos propios y datos oficiales) "
            "para obtener insights y conclusiones."
        ),
        "step_header": "🚀 Paso a paso: Cómo usar Geo-Agent-AI",
        "step_1": "1) Abre la aplicación ejecutando:\n```bash\ncd C:\\Users\\jesic\\Downloads\\GeoagentX\nconda activate GEOAgIX\nstreamlit run main.py\n```",
        "step_2": "2) Selecciona el idioma en la barra lateral (“Español” o “English”).",
        "step_3": "3) Ingresa y confirma la ubicación (ciudad o coordenadas) en el cuadro de texto.",
        "step_4": "4) Navega por las pestañas:\n   • **Buscar Noticias**: busca artículos, obtén resúmenes y tendencia.\n"
                  "   • **Subir Información**: carga imágenes, audios y textos; genera descripciones y mapa.\n"
                  "   • **Datos Oficiales**: consulta datos numéricos simulados o capas de riesgos de inundación.\n"
                  "   • **Contraste**: combina todos los inputs para un análisis comparativo.",
        "step_5": "5) Sigue las instrucciones dentro de cada pestaña para procesar la información.",

        # Ubicación
        "input_location_subheader": "1) Ingresa la ubicación principal",
        "input_location_placeholder": "Ejemplo: Ciudad de México, Guadalajara, Monterrey o coordenadas (lat, lon)",
        "btn_confirm_location": "Confirmar Ubicación",
        "msg_empty_location": "Por favor, escribe una ubicación válida.",
        "msg_location_set": "Ubicación establecida en: {}",
        "msg_no_location": "👆 Por favor, ingresa y confirma la ubicación para continuar con los agentes.",

        # Pestañas
        "tab_news": "Buscar Noticias",
        "tab_upload": "Subir Información",
        "tab_public": "Datos Oficiales",
        "tab_contrast": "Contraste",

        # Buscar Noticias
        "news_header": "🔍 Agente: Buscar Noticias",
        "news_keywords": "Palabras clave (e.g., huracán, inundación)",
        "news_start_date": "Fecha inicio (opcional)",
        "news_end_date": "Fecha fin (opcional)",
        "btn_search_news": "Ejecutar Búsqueda de Noticias",
        "insight_news": "Insight general de noticias",
        "articles_found": "Artículos encontrados",
        "trend_news": "Tendencia de Publicaciones",
        "msg_no_news": "No se encontraron artículos para esos parámetros.",

        # Subir Información
        "upload_header": "📤 Agente: Subir Información Multimodal",
        "upload_description": "Aquí puedes subir **imágenes**, **audios** y **textos** relacionados con la ubicación: **{}**",
        "upload_images": "Imágenes (png, jpg, jpeg)",
        "upload_audios": "Audios (mp3, wav)",
        "upload_texts": "Archivos de Texto (.txt)",
        "upload_coords": "Coordenadas (lat, lon) donde se tomó la información (opcional)",
        "btn_process_uploads": "Procesar Archivos Subidos",
        "multimodal_analysis": "Análisis Multimodal",
        "msg_no_uploads": "No se subió información para procesar.",
        "map_resources": "Mapa de Recursos Georreferenciados",
        "summary_uploads": "Resumen General de lo Subido",

        # Datos Oficiales
        "public_header": "📊 Agente: Consultar Datos Oficiales",
        "public_description": "Obtén datos oficiales para **{}**",
        "select_public_type": "Tipo de dato",
        "public_types": ["Demográficos", "Meteorológicos", "Sísmicos", "Económicos", "Riesgos de Inundación"],
        "public_years": "Período a mostrar (años atrás)",
        "btn_get_public": "Obtener Datos Oficiales",
        "geo_coords": "**Coordenadas de `{}`:** {:.6f}, {:.6f}",
        "geo_display_name": "**Nombre completo:** {}",
        "msg_no_public": "No hay datos oficiales para mostrar.",
        "public_table": "Datos en Tabla",
        "public_trend": "Gráfico de Tendencia",
        "public_no_graph": "No se generó gráfico para estos datos oficiales.",
        "flood_header": "Mapa de Riesgos de Inundación (GeoJSON)",
        "flood_no_geojson": "No se pudo descargar o procesar el GeoJSON de inundaciones.",

        # Contraste
        "contrast_header": "🔄 Contraste y Análisis de Información Combinada",
        "msg_no_agents_run": "Para ver el contraste, primero debes correr al menos uno de los agentes anteriores.",
        "summary_available": "Resumen rápido de inputs disponibles:",
        "news_available": "- Noticias encontradas: {} artículos.",
        "news_no_data": "- Noticias: Sin datos.",
        "multimodal_available": "- Información propia subida: {} items.",
        "multimodal_no_data": "- Información multimodal: Sin datos.",
        "public_num_available": "- Datos oficiales (numéricos): {} registros.",
        "public_geo_available": "- Datos oficiales (GeoJSON de inundaciones) disponibles.",
        "public_no_data2": "- Datos oficiales: Sin datos.",
        "btn_contrast": "Generar Comentario de Contraste",
        "contrast_news": "Noticias:\n{}",
        "contrast_multimodal": "Información Propia:\n{}",
        "contrast_public_num": "Datos Oficiales (numéricos):\n{}",
        "contrast_public_geo": "Datos Oficiales (GeoJSON de inundaciones) disponibles.",
        "contrast_prompt": "Contrasta la información de las noticias, la información propia y los datos oficiales para la ubicación {}.\n\n{}\n\nResume las similitudes, diferencias y posibles conclusiones.",
        "result_contrast": "Resultado del Análisis de Contraste",
        "combined_viz": "Visualizaciones Combinadas (ejemplo)",
        "trend_news_viz": "**Tendencia de Noticias**",
        "trend_public_viz": "**Tendencia de Datos Oficiales (numéricos)**",
        "flood_map_viz": "**Mapa de Riesgos de Inundación**",
        "resources_map_viz": "**Mapa de Recursos Propios (puntos)**",
        "end_info": "Puedes regresar a cada pestaña de los agentes para actualizar los datos y luego volver aquí para regenerar el contraste."
    },
    "en": {
        "app_title": "Geo-Agent-AI: Multi-agent Local Data App",
        "select_lang": "Selecciona idioma / Select language",
        "spanish": "Español",
        "english": "English",

        # Introduction
        "intro_header": "📄 Introduction to Geo-Agent-AI",
        "intro_text": (
            "Geo-Agent-AI is a **multi-agent multimodal application** designed to empower "
            "communities and organizations to:\n\n"
            "1. **Search and process news** for a specific location.\n"
            "2. **Upload their own data** (images, audio, text) tied to a chosen location.\n"
            "3. **Fetch official data and geospatial layers** (e.g., flood risk) to contrast information.\n"
            "4. **Perform a combined analysis** of the three sources (news, user data, and official data) "
            "to gain insights and conclusions."
        ),
        "step_header": "🚀 Step by Step: How to Use Geo-Agent-AI",
        "step_1": "1) Open the app by running:\n```bash\ncd C:\\Users\\jesic\\Downloads\\GeoagentX\nconda activate GEOAgIX\nstreamlit run main.py\n```",
        "step_2": "2) Select your language in the sidebar (“Español” or “English”).",
        "step_3": "3) Enter and confirm your location (city or coordinates) in the text box.",
        "step_4": "4) Navigate through the tabs:\n   • **Search News**: lookup articles, get summaries and trends.\n"
                  "   • **Upload Data**: upload images, audio, and text; generate descriptions and a map.\n"
                  "   • **Official Data**: fetch numeric simulations or flood-risk layers.\n"
                  "   • **Contrast**: combine all inputs for a comparative analysis.",
        "step_5": "5) Follow the instructions in each tab to process your data.",

        # Location
        "input_location_subheader": "1) Enter the main location",
        "input_location_placeholder": "Example: Mexico City, Guadalajara, Monterrey or coordinates (lat, lon)",
        "btn_confirm_location": "Confirm Location",
        "msg_empty_location": "Please enter a valid location.",
        "msg_location_set": "Location set to: {}",
        "msg_no_location": "👆 Please enter and confirm the location to continue with the agents.",

        # Tabs
        "tab_news": "Search News",
        "tab_upload": "Upload Data",
        "tab_public": "Official Data",
        "tab_contrast": "Contrast",

        # Search News
        "news_header": "🔍 Agent: Search News",
        "news_keywords": "Keywords (e.g., hurricane, flood)",
        "news_start_date": "Start date (optional)",
        "news_end_date": "End date (optional)",
        "btn_search_news": "Run News Search",
        "insight_news": "News global insight",
        "articles_found": "Articles found",
        "trend_news": "Publication Trend",
        "msg_no_news": "No articles found for those parameters.",

        # Upload Data
        "upload_header": "📤 Agent: Upload Multimodal Data",
        "upload_description": "Here you can upload **images**, **audios**, and **texts** related to the location: **{}**",
        "upload_images": "Images (png, jpg, jpeg)",
        "upload_audios": "Audios (mp3, wav)",
        "upload_texts": "Text Files (.txt)",
        "upload_coords": "Coordinates (lat, lon) where the data was collected (optional)",
        "btn_process_uploads": "Process Uploaded Files",
        "multimodal_analysis": "Multimodal Analysis",
        "msg_no_uploads": "No data was uploaded for processing.",
        "map_resources": "Georeferenced Data Map",
        "summary_uploads": "General Summary of Uploads",

        # Official Data
        "public_header": "📊 Agent: Fetch Official Data",
        "public_description": "Get official data for **{}**",
        "select_public_type": "Data type",
        "public_types": ["Demographics", "Meteorological", "Seismic", "Economic", "Flood Risks"],
        "public_years": "Period to display (years back)",
        "btn_get_public": "Fetch Official Data",
        "geo_coords": "**Coordinates of `{}`:** {:.6f}, {:.6f}",
        "geo_display_name": "**Full name:** {}",
        "msg_no_public": "No official data to display.",
        "public_table": "Data Table",
        "public_trend": "Trend Chart",
        "public_no_graph": "No chart generated for these official data.",
        "flood_header": "Flood Risk Map (GeoJSON)",
        "flood_no_geojson": "Could not download or process the flood GeoJSON.",

        # Contrast
        "contrast_header": "🔄 Contrast and Combined Analysis",
        "msg_no_agents_run": "To view contrast, you must first run at least one of the previous agents.",
        "summary_available": "Quick summary of available inputs:",
        "news_available": "- News found: {} articles.",
        "news_no_data": "- News: No data.",
        "multimodal_available": "- User-uploaded data: {} items.",
        "multimodal_no_data": "- Multimodal data: No data.",
        "public_num_available": "- Official data (numeric): {} records.",
        "public_geo_available": "- Official data (flood GeoJSON) available.",
        "public_no_data2": "- Official data: No data.",
        "btn_contrast": "Generate Contrast Commentary",
        "contrast_news": "News:\n{}",
        "contrast_multimodal": "User Data:\n{}",
        "contrast_public_num": "Official Data (numeric):\n{}",
        "contrast_public_geo": "Official data (flood GeoJSON) available.",
        "contrast_prompt": "Contrast the information from news, user data, and official data for location {}.\n\n{}\n\nSummarize similarities, differences, and possible conclusions.",
        "result_contrast": "Contrast Analysis Result",
        "combined_viz": "Combined Visualizations (example)",
        "trend_news_viz": "**News Trend**",
        "trend_public_viz": "**Official Data Trend (numeric)**",
        "flood_map_viz": "**Flood Risk Map**",
        "resources_map_viz": "**User Resources Map (points)**",
        "end_info": "You can return to each agent tab to refresh data and then come back here to regenerate the contrast."
    }
}

# ─────────── Selección de idioma ───────────
st.set_page_config(
    page_title=TEXTS["es"]["app_title"],
    page_icon="🤖",
    layout="wide"
)

lang_choice = st.sidebar.selectbox(
    TEXTS["es"]["select_lang"],
    (TEXTS["es"]["spanish"], TEXTS["es"]["english"]),
    index=0
)
lang_code = "es" if lang_choice == TEXTS["es"]["spanish"] else "en"
t = TEXTS[lang_code]

# ─────────── Título principal ───────────
# Mostrar imagen de cabecera si existe
if os.path.exists(os.path.join(PROJECT_ROOT, "mapa.jpg")):
    st.image(os.path.join(PROJECT_ROOT, "mapa.jpg"), use_container_width=True)
else:
    st.warning("⚠️ No se encontró `mapa.jpg` en la carpeta principal.")

st.title(t["app_title"])

# ─────────── Introducción e imágenes ───────────
st.subheader(t["intro_header"])
st.markdown(t["intro_text"])

# Mostrar imagen en la barra lateral si existe
if os.path.exists(os.path.join(PROJECT_ROOT, "Mapacomunidad.png")):
    st.sidebar.image(os.path.join(PROJECT_ROOT, "Mapacomunidad.png"), use_container_width=True)
    st.image(os.path.join(PROJECT_ROOT, "analitica.png"), use_container_width=True)
    st.image(os.path.join(PROJECT_ROOT, "logocentrus.png"), use_container_width=True)
else:
    st.sidebar.warning("⚠️ No se encontró `Mapacomunidad.png` en la carpeta principal.")

# ─────────── Paso a paso ───────────
st.subheader(t["step_header"])
st.markdown(t["step_1"])
st.markdown(t["step_2"])
st.markdown(t["step_3"])
st.markdown(t["step_4"])
st.markdown(t["step_5"])

st.markdown("---")  # Línea divisoria

# ─────────── PASO 1: INPUT GLOBAL DE UBICACIÓN ───────────
if "ubicacion" not in st.session_state:
    st.session_state["ubicacion"] = ""

st.subheader(t["input_location_subheader"])
ubicacion_input = st.text_input(
    t["input_location_placeholder"],
    value=st.session_state["ubicacion"]
)

if st.button(t["btn_confirm_location"]):
    if ubicacion_input.strip() == "":
        st.error(t["msg_empty_location"])
    else:
        st.session_state["ubicacion"] = ubicacion_input.strip()
        st.success(t["msg_location_set"].format(st.session_state["ubicacion"]))

if not st.session_state["ubicacion"]:
    st.info(t["msg_no_location"])
    st.stop()

# ─────────── PASO 2: PESTAÑAS DE AGENTES ───────────
tab1, tab2, tab3, tab4 = st.tabs([
    t["tab_news"],
    t["tab_upload"],
    t["tab_public"],
    t["tab_contrast"]
])

# --- 2.1 Pestaña 1: Buscar Noticias ---
with tab1:
    st.header(t["news_header"])
    keywords = st.text_input(t["news_keywords"], key="keywords_news")
    fecha_inicio = st.date_input(t["news_start_date"], key="fi_news")
    fecha_fin = st.date_input(t["news_end_date"], key="ff_news")
    if st.button(t["btn_search_news"], key="btn_buscar_noticias"):
        with st.spinner(f"{t['news_header']}..."):
            news_output = fetch_and_process_news(
                st.session_state["ubicacion"],
                keywords,
                fecha_inicio,
                fecha_fin
            )
            st.session_state["news_output"] = news_output

        st.subheader(t["insight_news"])
        st.markdown(news_output["texto_summary"])

        st.subheader(t["articles_found"])
        df_n = news_output["df_articulos"]
        if df_n.empty:
            st.write(t["msg_no_news"])
        else:
            st.dataframe(
                df_n[["fecha", "fuente", "titulo", "resumen", "url"]],
                use_container_width=True
            )

        st.subheader(t["trend_news"])
        fig_n = news_output["fig_time_series"]
        if fig_n and hasattr(fig_n, "to_plotly_json"):
            st.plotly_chart(fig_n, use_container_width=True, key="plot_news_trend")
        else:
            st.write(t["msg_no_news"])

# --- 2.2 Pestaña 2: Subir Información ---
with tab2:
    st.header(t["upload_header"])
    st.markdown(t["upload_description"].format(st.session_state["ubicacion"]))
    images = st.file_uploader(
        t["upload_images"],
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True,
        key="up_images"
    )
    audios = st.file_uploader(
        t["upload_audios"],
        type=["mp3", "wav"],
        accept_multiple_files=True,
        key="up_audios"
    )
    textos = st.file_uploader(
        t["upload_texts"],
        type=["txt"],
        accept_multiple_files=True,
        key="up_textos"
    )
    coords_input = st.text_input(
        t["upload_coords"],
        key="up_coords"
    )

    if st.button(t["btn_process_uploads"], key="btn_procesar_multimodal"):
        with st.spinner(f"{t['upload_header']}..."):
            multimodal_output = process_user_uploads(
                st.session_state["ubicacion"],
                images,
                audios,
                textos,
                coords_input
            )
            st.session_state["multimodal_output"] = multimodal_output

        st.subheader(t["multimodal_analysis"])

        df_m = multimodal_output["df_multimodal"]
        if df_m.empty:
            st.write(t["msg_no_uploads"])
        else:
            st.dataframe(
                df_m[["tipo", "archivo", "lat", "lon", "descripcion"]],
                use_container_width=True
            )

            # ──── MAPA con st.map (Streamlit) ────
            df_mapa = df_m.dropna(subset=["lat", "lon"])[["lat", "lon"]]
            if not df_mapa.empty:
                st.subheader(t["map_resources"])
                st.map(df_mapa)

        st.subheader(t["summary_uploads"])
        st.markdown(multimodal_output["texto_summary"])

# --- 2.3 Pestaña 3: Datos Oficiales ---
with tab3:
    st.header(t["public_header"])
    st.markdown(t["public_description"].format(st.session_state["ubicacion"]))
    tipo_dato = st.selectbox(
        t["select_public_type"],
        t["public_types"],
        key="sel_tipo_dato"
    )
    periodo = st.slider(
        t["public_years"],
        min_value=1,
        max_value=10,
        value=5,
        key="slider_periodo"
    )

    if st.button(t["btn_get_public"], key="btn_datos_oficiales"):
        with st.spinner(f"{t['public_header']}..."):
            public_output = fetch_public_data(
                st.session_state["ubicacion"],
                tipo_dato,
                periodo
            )
            st.session_state["public_output"] = public_output

        df_p = public_output["df"]
        fig_p = public_output["fig"]
        geo_info = public_output["geo_info"]

        # Mostrar info de geocodificación
        if geo_info:
            st.markdown(
                t["geo_coords"].format(
                    st.session_state["ubicacion"],
                    geo_info.get("lat", 0.0),
                    geo_info.get("lon", 0.0)
                )
            )
            if geo_info.get("display_name"):
                st.markdown(t["geo_display_name"].format(geo_info["display_name"]))

        if tipo_dato != t["public_types"][-1]:  # Si no es "Riesgos de Inundación"
            if df_p.empty:
                st.write(t["msg_no_public"])
            else:
                st.subheader(t["public_table"])
                st.dataframe(df_p, use_container_width=True)

                st.subheader(t["public_trend"])
                if fig_p and hasattr(fig_p, "to_plotly_json"):
                    st.plotly_chart(fig_p, use_container_width=True, key="plot_public_trend")
                else:
                    st.write(t["public_no_graph"])
        else:
            # Caso "Riesgos de Inundación" → GeoJSON + PyDeck
            if fig_p and isinstance(fig_p, dict) and fig_p.get("geojson"):
                st.subheader(t["flood_header"])
                layer = pdk.Layer(
                    "GeoJsonLayer",
                    data=fig_p["geojson"],
                    pickable=True,
                    stroked=False,
                    filled=True,
                    extruded=False,
                    get_fill_color=[255, 0, 0, 100]
                )
                view_state = pdk.ViewState(
                    latitude=fig_p["view_state"]["latitude"],
                    longitude=fig_p["view_state"]["longitude"],
                    zoom=fig_p["view_state"]["zoom"],
                    pitch=0
                )
                deck = pdk.Deck(
                    layers=[layer],
                    initial_view_state=view_state,
                    map_style="mapbox://styles/mapbox/light-v10"
                )
                st.pydeck_chart(deck, key="deck_flood")
            else:
                st.write(t["flood_no_geojson"])

# --- 2.4 Pestaña 4: Contraste y Análisis ---
with tab4:
    st.header(t["contrast_header"])
    noticias_ok = (
        "news_output" in st.session_state
        and st.session_state["news_output"]["df_articulos"].shape[0] > 0
    )
    multimodal_ok = (
        "multimodal_output" in st.session_state
        and st.session_state["multimodal_output"]["df_multimodal"].shape[0] > 0
    )
    public_ok = (
        "public_output" in st.session_state
        and (
            ("df" in st.session_state["public_output"]
             and st.session_state["public_output"]["df"].shape[0] > 0)
            or ("fig" in st.session_state["public_output"]
                and isinstance(st.session_state["public_output"]["fig"], dict)
                and st.session_state["public_output"]["fig"].get("geojson"))
        )
    )

    if not (noticias_ok or multimodal_ok or public_ok):
        st.info(t["msg_no_agents_run"])
        st.stop()

    st.subheader(t["summary_available"])
    if noticias_ok:
        cnt_n = st.session_state["news_output"]["df_articulos"].shape[0]
        st.write(t["news_available"].format(cnt_n))
    else:
        st.write(t["news_no_data"])

    if multimodal_ok:
        cnt_m = st.session_state["multimodal_output"]["df_multimodal"].shape[0]
        st.write(t["multimodal_available"].format(cnt_m))
    else:
        st.write(t["multimodal_no_data"])

    if public_ok:
        po = st.session_state["public_output"]
        if "df" in po and not po["df"].empty:
            cnt_p = po["df"].shape[0]
            st.write(t["public_num_available"].format(cnt_p))
        elif "fig" in po and isinstance(po["fig"], dict) and po["fig"].get("geojson"):
            st.write(t["public_geo_available"])
        else:
            st.write(t["public_no_data2"])
    else:
        st.write(t["public_no_data2"])

    # ──── Generar comentario de contraste con LLM ────
    if st.button(t["btn_contrast"], key="btn_contraste_llm"):
        partes = []
        if noticias_ok:
            news_res = "\n".join(
                st.session_state["news_output"]["df_articulos"]["resumen"].tolist()[:5]
            )
            partes.append(t["contrast_news"].format(news_res))
        if multimodal_ok:
            user_res = "\n".join(
                st.session_state["multimodal_output"]["df_multimodal"]["descripcion"].tolist()[:5]
            )
            partes.append(t["contrast_multimodal"].format(user_res))
        if public_ok:
            po = st.session_state["public_output"]
            if "df" in po and not po["df"].empty:
                last_rows = "\n".join(
                    f"{row['fecha'].year}: {row['valor']}"
                    for _, row in po["df"].tail(5).iterrows()
                )
                partes.append(t["contrast_public_num"].format(last_rows))
            elif "fig" in po and isinstance(po["fig"], dict) and po["fig"].get("geojson"):
                partes.append(t["contrast_public_geo"])
            else:
                partes.append(t["public_no_data2"])

        texto_contra = "\n\n---\n\n".join(partes)
        from utils.llm import analyze_text_with_llm
        resultado_contraste = analyze_text_with_llm(
            t["contrast_prompt"].format(
                st.session_state["ubicacion"],
                texto_contra
            )
        )
        st.subheader(t["result_contrast"])
        st.markdown(resultado_contraste, unsafe_allow_html=True)

    st.subheader(t["combined_viz"])

    if noticias_ok:
        st.markdown(t["trend_news_viz"])
        fig_n2 = st.session_state["news_output"]["fig_time_series"]
        if fig_n2 and hasattr(fig_n2, "to_plotly_json"):
            st.plotly_chart(fig_n2, use_container_width=True, key="plot_news_combined")

    if public_ok:
        po = st.session_state["public_output"]
        # Datos numéricos
        if "df" in po and not po["df"].empty:
            st.markdown(t["trend_public_viz"])
            fig_p2 = po["fig"]
            if fig_p2 and hasattr(fig_p2, "to_plotly_json"):
                st.plotly_chart(fig_p2, use_container_width=True, key="plot_public_combined")
        # GeoJSON inundaciones
        if "fig" in po and isinstance(po["fig"], dict) and po["fig"].get("geojson"):
            st.markdown(t["flood_map_viz"])
            layer2 = pdk.Layer(
                "GeoJsonLayer",
                data=po["fig"]["geojson"],
                pickable=True,
                stroked=False,
                filled=True,
                extruded=False,
                get_fill_color=[255, 0, 0, 100]
            )
            view_state2 = pdk.ViewState(
                latitude=po["fig"]["view_state"]["latitude"],
                longitude=po["fig"]["view_state"]["longitude"],
                zoom=po["fig"]["view_state"]["zoom"],
                pitch=0
            )
            deck2 = pdk.Deck(
                layers=[layer2],
                initial_view_state=view_state2,
                map_style="mapbox://styles/mapbox/light-v10"
            )
            st.pydeck_chart(deck2, key="deck_flood_combined")

    if multimodal_ok:
        st.markdown(t["resources_map_viz"])
        df_m = st.session_state["multimodal_output"]["df_multimodal"]
        df_map = df_m.dropna(subset=["lat", "lon"])[["lat", "lon", "descripcion"]]
        if not df_map.empty:
            st.map(df_map)

    st.write("---")
    st.info(t["end_info"])
