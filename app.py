import streamlit as st
import streamlit.components.v1 as components
from red_politica import generar_html_red

st.set_page_config(page_title="Inteligencia SLP", layout="wide")

st.title("Centro de Inteligencia: Red Morena SLP")
st.markdown("""
**Guía de Colores de Hilos:**
* 🔴 **Rojo:** Padrinazgo / Vínculo Familiar Directo
* 🔵 **Azul:** Alianza Operativa / Estructura de Trabajo
* 🟢 **Verde:** Flujo de Recursos / Financiamiento
* ⬛ **Gris Oscuro:** Puntos de Tensión / Competencia Interna
""")

# Generar y renderizar la pizarra interactiva
path_mapa = generar_html_red()

with open(path_mapa, 'r', encoding='utf-8') as f:
    html_code = f.read()
    
components.html(html_code, height=700, scrolling=False)