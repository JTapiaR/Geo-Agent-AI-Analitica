# agents/news_agent.py

import feedparser
import pandas as pd
from datetime import datetime
import plotly.express as px

from utils.llm import summarize_with_llm, extract_entities

def fetch_and_process_news(lugar: str, keywords: str, fecha_inicio, fecha_fin):
    """
    Obtiene noticias gratuitas de Google News RSS según 'keywords' y 'lugar',
    las procesa en un DataFrame, genera resúmenes/entidades con LLM, un insight global
    y construye un gráfico de tendencia de noticias por fecha.
    
    Parámetros:
      - lugar (str): Ciudad, región o término geográfico para filtrar.
      - keywords (str): Palabras clave adicionales.
      - fecha_inicio (datetime.date): Fecha mínima para filtrar (opcional).
      - fecha_fin (datetime.date): Fecha máxima para filtrar (opcional).
    
    Retorna un diccionario con:
      - texto_summary: insight global generado por LLM.
      - df_articulos: DataFrame con información de cada noticia.
      - fig_time_series: figura de Plotly con la tendencia diaria de noticias.
    """

    # 1) Construir la URL del RSS de Google News
    #    hl=es-419 (idioma español Latinoamérica), gl=MX (país México), ceid=MX:es
    #    Buscamos "keywords" AND "lugar"
    query = f"{keywords} {lugar}".strip().replace(" ", "+")
    rss_url = (
        "https://news.google.com/rss/search?"
        f"q={query}&hl=es-419&gl=MX&ceid=MX:es"
    )

    # 2) Leer el feed RSS con feedparser
    feed = feedparser.parse(rss_url)
    entries = feed.get("entries", [])

    # 3) Filtrar por rango de fechas si se suministraron
    rows = []
    for entry in entries:
        # 'published_parsed' es una tupla struct_time, convertimos a datetime
        try:
            published_dt = datetime(*entry.published_parsed[:6])
        except Exception:
            # Si no pudiera parsear la fecha, la omitimos
            continue

        # Si se proporcionó fecha_inicio/fecha_fin, comparamos
        if fecha_inicio:
            dt_inicio = datetime.combine(fecha_inicio, datetime.min.time())
            if published_dt < dt_inicio:
                continue
        if fecha_fin:
            dt_fin = datetime.combine(fecha_fin, datetime.max.time())
            if published_dt > dt_fin:
                continue

        # Extraer título, descripción (summary), link y fuente
        titulo = entry.get("title", "")
        descripcion = entry.get("summary", "")
        url = entry.get("link", "")
        fuente = entry.get("source", {}).get("title", "") if entry.get("source") else ""
        
        rows.append({
            "titulo": titulo,
            "descripcion": descripcion,
            "url": url,
            "fecha": published_dt,
            "fuente": fuente or entry.get("author", "")
        })

    # 4) Crear DataFrame
    df = pd.DataFrame(rows)

    # Si no hay resultados, devolvemos estructuras vacías
    if df.empty:
        return {
            "texto_summary": "No se encontraron noticias para esos parámetros.",
            "df_articulos": df,
            "fig_time_series": {}  # figura vacía
        }

    # 5) Ordenar por fecha descendente
    df = df.sort_values(by="fecha", ascending=False).reset_index(drop=True)

    # 6) Llamadas a LLM para resumen y extracción de entidades
    res_summaries = []
    entidades = []
    for idx, row in df.iterrows():
        # Texto largo para LLM
        texto_largo = row["titulo"] + ". " + (row["descripcion"] or "")
        resumen = summarize_with_llm(texto_largo)
        ent = extract_entities(texto_largo)
        res_summaries.append(resumen)
        entidades.append(ent)

    df["resumen"] = res_summaries
    df["entidades"] = entidades

    # 7) Generar insight global con los primeros 10 resúmenes
    top_summaries = res_summaries[:10] if len(res_summaries) >= 10 else res_summaries
    texto_concatenado = "\n".join(top_summaries)
    insight_global = summarize_with_llm(
        f"Con base en estos resúmenes:\n{texto_concatenado}\n\n"
        "Genera un insight general sobre la situación."
    )

    # 8) Construir gráfico de tendencia diaria
    df_count = (
        df.groupby(df["fecha"].dt.date)
          .size()
          .reset_index(name="conteo")
          .rename(columns={"fecha": "fecha_dia"})
    )

    fig_time_series = px.line(
        df_count,
        x="fecha_dia",
        y="conteo",
        title=f"Tendencia diaria de noticias sobre \"{keywords}\" en \"{lugar}\"",
        markers=True
    )
    fig_time_series.update_layout(
        xaxis_title="Fecha",
        yaxis_title="Cantidad de artículos",
        xaxis=dict(tickformat="%Y-%m-%d"),
        template="plotly_white"
    )

    # 9) Retornar el diccionario con resultados
    return {
        "texto_summary": insight_global,
        "df_articulos": df,
        "fig_time_series": fig_time_series
    }

