# utils/vision_utils.py

from PIL import Image
import os

def analyze_image(image_path: str) -> str:
    """
    Abre la imagen usando Pillow y devuelve:
      - Resolución (ancho x alto)
      - Modo de color (RGB, L, etc.)
      - Los 3 colores dominantes (en RGB hex) mediante quantize().
    Si ocurre algún error, retorna un mensaje de advertencia.
    """

    if not os.path.isfile(image_path):
        return f"⚠️ No se encontró el archivo: {image_path}"

    try:
        img = Image.open(image_path).convert("RGB")
    except Exception as e:
        return f"⚠️ No se pudo abrir la imagen: {e}"

    try:
        # 1) Información básica
        ancho, alto = img.size
        modo = img.mode  # típicamente "RGB" para fotografías

        # 2) Obtener paleta reducida a 3 colores dominantes
        #    quantize() reduce la cantidad de colores para luego extraerlos via getpalette()
        small = img.copy().resize((128, 128))  # reducir resolución para acelerar
        paleta = small.quantize(colors=3, method=Image.MEDIANCUT).getpalette()
        # paleta es lista de [R0, G0, B0, R1, G1, B1, R2, G2, B2, ...]
        # getcolors() sobre la imagen quantizada da (pixel_count, index_color)
        colores = small.quantize(colors=3, method=Image.MEDIANCUT).getcolors(128*128)
        # Ordenar por frecuencia descendente
        colores.sort(reverse=True, key=lambda tup: tup[0])
        dominantes = []
        for count, idx in colores[:3]:
            r = paleta[3*idx]
            g = paleta[3*idx + 1]
            b = paleta[3*idx + 2]
            dominantes.append(f"#{r:02x}{g:02x}{b:02x}")

        descripcion = (
            f"Resolución: {ancho}×{alto}px. Modo: {modo}. "
            f"Colores dominantes: {', '.join(dominantes)}."
        )
        return descripcion
    except Exception as e:
        return f"⚠️ Error al analizar la imagen: {e}"


