# utils/llm_utils.py

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# 1) Leer API Key de OpenAI


api_key = os.getenv("OPENAI_API_KEY")
# 2) Crear cliente global
client = OpenAI(api_key=api_key)


def summarize_with_llm(texto: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres un asistente que resume textos de forma concisa."},
            {"role": "user", "content": texto}
        ],
        temperature=0.3,
        max_tokens=150
    )
    return response.choices[0].message.content.strip()


def extract_entities(texto: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Eres un asistente experto en extracción de entidades (lugares, fechas, organizaciones)."
            },
            {"role": "user", "content": f"Extrae las entidades del siguiente texto:\n\n{texto}"}
        ],
        temperature=0.0
    )
    return response.choices[0].message.content.strip()


def transcribe_audio_whisper(audio_path: str) -> str:
    with open(audio_path, "rb") as audio_file:
        resp = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-1"
        )
    return resp.text


def analyze_text_with_llm(texto: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres un analista que extrae insights y resume textos."},
            {"role": "user", "content": texto}
        ]
    )
    return response.choices[0].message.content.strip()
