import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans

def run_analytics(public_data_output):
    df = public_data_output["df"]
    # Ejemplo: Generar gráfico de serie de tiempo
    fig = px.line(df, x="fecha", y="valor", title="Tendencia de Indicador Público")

    # Calcular clustering (si tiene sentido) o anomalías
    # ...
    # df["cluster"] = KMeans(n_clusters=2).fit_predict(df[["valor"]])

    conclusiones = f"El promedio del indicador en los últimos periodos es {df['valor'].mean():.2f}. "
    # Podéis pedir al LLM un análisis más cualitativo si queréis.

    return {
        "fig_principal": fig,
        "df_detalle": df,
        "texto_conclusiones": conclusiones
    }
