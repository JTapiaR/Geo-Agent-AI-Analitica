# agents/user_data_agent.py

import os
import pandas as pd
from utils.vision_utils import analyze_image
from utils.llm import transcribe_audio_whisper, analyze_text_with_llm

def process_user_uploads(ubicacion: str, images, audios, textos, coords_input):
    """
    Procesa archivos subidos por el usuario dentro del contexto de 'ubicacion'.
    - Para imágenes: extrae metadatos y colores dominantes con PIL.
    - Para audios: transcribe con Whisper + resume con LLM.
    - Para textos: analiza con LLM.
    Retorna:
      - df_multimodal: DataFrame con columnas [tipo, archivo, lat, lon, descripcion]
      - texto_summary: resumen general de todas las descripciones.
    """

    # 1) Parsear coordenadas (si vienen como "lat, lon")
    try:
        lat, lon = map(float, coords_input.split(","))
    except Exception:
        lat, lon = (None, None)

    registros = []

    # 2) Procesar imágenes
    for img_file in images:
        temp_path = os.path.join("data", img_file.name)
        os.makedirs(os.path.dirname(temp_path), exist_ok=True)
        with open(temp_path, "wb") as f:
            f.write(img_file.getbuffer())

        # Descripción básica con PIL
        descripcion_img = analyze_image(temp_path)

        registros.append({
            "tipo": "imagen",
            "archivo": img_file.name,
            "lat": lat,
            "lon": lon,
            "descripcion": descripcion_img
        })

    # 3) Procesar audios
    for audio_file in audios:
        temp_path = os.path.join("data", audio_file.name)
        os.makedirs(os.path.dirname(temp_path), exist_ok=True)
        with open(temp_path, "wb") as f:
            f.write(audio_file.getbuffer())

        transcript = transcribe_audio_whisper(temp_path)
        summary_audio = analyze_text_with_llm(transcript)

        registros.append({
            "tipo": "audio",
            "archivo": audio_file.name,
            "lat": lat,
            "lon": lon,
            "descripcion": summary_audio
        })

    # 4) Procesar textos
    for txt_file in textos:
        try:
            content = txt_file.read().decode("utf-8")
        except Exception:
            content = ""
        analysis_text = analyze_text_with_llm(content)

        registros.append({
            "tipo": "texto",
            "archivo": txt_file.name,
            "lat": lat,
            "lon": lon,
            "descripcion": analysis_text
        })

    # 5) Construir DataFrame
    df = pd.DataFrame(registros)

    # 6) Generar resumen general (si hay registros)
    if not df.empty:
        todos_textos = "\n".join(df["descripcion"].tolist())
        resumen_general = analyze_text_with_llm(
            f"Con base en estas descripciones de archivos subidos en {ubicacion}: {todos_textos}\n"
            "Resume los hallazgos principales."
        )
    else:
        resumen_general = "No se subió información para procesar."

    return {
        "df_multimodal": df,
        "texto_summary": resumen_general
    }
