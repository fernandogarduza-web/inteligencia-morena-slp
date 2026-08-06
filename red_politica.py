import os
import tempfile
import networkx as nx
import pandas as pd
from pyvis.network import Network

def obtener_datos_red():
    """
    Define los nodos (personajes/instituciones) y las aristas (relaciones) del mapa político.
    """
    # Ruta base de tus imágenes en GitHub
    base_url = "https://raw.githubusercontent.com/fernandogarduza-web/inteligencia-morena-slp/main/perfiles_morena/"

    # 1. Definición de Nodos Completos
    nodos = [
        # Cúpula Federal
        {"id": "Rosa Icela Rodríguez", "faccion": "Cúpula Federal", "cargo": "Titular de SEGOB", "color": "#d9534f", "size": 35, "foto": f"{base_url}rosa_icela.jpg"},
        {"id": "Ernestina Godoy", "faccion": "Cúpula Federal", "cargo": "Consejera Jurídica Presidencia", "color": "#d9534f", "size": 30, "foto": f"{base_url}ernestina_godoy.jpg"},
        
        # Dirigencia y Cuadros Puros
        {"id": "Rita Ozalia Rodríguez", "faccion": "Ala Pura / Dirigencia", "cargo": "Presidenta CEE Morena SLP", "color": "#8b0000", "size": 30, "foto": f"{base_url}rita_ozalia.jpg"},
        {"id": "Carlos Arreola", "faccion": "Ala Pura / Dirigencia", "cargo": "Diputado con licencia", "color": "#8b0000", "size": 25, "foto": f"{base_url}carlos_arreola.jpg"},
        {"id": "Paloma Aguilar", "faccion": "Ala Pura / Dirigencia", "cargo": "Ex SAT / Perfil Histórico", "color": "#8b0000", "size": 20, "foto": f"{base_url}paloma_aguilar.jpg"},
        
        # Grupo Gabino / Estructura Territorial
        {"id": "Gabino Morales", "faccion": "Grupo Gabino", "cargo": "Diputado Federal", "color": "#0275d8", "size": 30, "foto": f"{base_url}gabino_morales.jpg"},
        {"id": "Guillermo Morales", "faccion": "Grupo Gabino", "cargo": "Delegado del Bienestar SLP", "color": "#0275d8", "size": 25, "foto": f"{base_url}guillermo_morales.jpg"},
        {"id": "Kevin Ángelo Aguilar", "faccion": "Grupo Gabino", "cargo": "Diputado Federal (Huasteca)", "color": "#0275d8", "size": 22, "foto": f"{base_url}kevin_angelo.jpg"},
        
        # Burocracia y Delegaciones Federales
        {"id": "Armando Navarro", "faccion": "Delegaciones Federales", "cargo": "Delegado de Banobras SLP", "color": "#f0ad4e", "size": 25, "foto": f"{base_url}armando_navarro.jpg"},
        {"id": "Elí César Cervantes", "faccion": "Delegaciones Federales", "cargo": "Director Centro SICT SLP", "color": "#f0ad4e", "size": 20, "foto": f"{base_url}eli_cesar.jpg"},
        {"id": "Mario Godoy", "faccion": "Delegaciones Federales", "cargo": "Representante INPI SLP", "color": "#f0ad4e", "size": 20, "foto": f"{base_url}mario_godoy.jpg"},
        
        # Legislativo Local, Alcaldes y Autónomos
        {"id": "Cuauhtli Badillo", "faccion": "Legislativo Local", "cargo": "Diputado Local (Aspirante Capital)", "color": "#5bc0de", "size": 22, "foto": f"{base_url}cuauhtli_badillo.jpg"},
        {"id": "Leonel Serrato", "faccion": "Perfil Independiente", "cargo": "Notario / Ex SCT Estatal", "color": "#5cb85c", "size": 22, "foto": f"{base_url}leonel_serrato.jpg"},
        {"id": "Juan Ramiro Robledo", "faccion": "Vieja Guardia", "cargo": "Legislador Federal Histórico", "color": "#d9534f", "size": 28, "foto": f"{base_url}juan_ramiro.jpg"},
        {"id": "Nancy Jeanine García", "faccion": "Ala Pura / Dirigencia", "cargo": "Diputada Local", "color": "#8b0000", "size": 20, "foto": f"{base_url}nancy_jeanine.jpg"},
        {"id": "Leticia Vázquez", "faccion": "Bases Municipales", "cargo": "Alcaldesa de Cerritos", "color": "#8b0000", "size": 22, "foto": f"{base_url}leticia_vazquez.jpg"},
        
        # Actores Financieros, Activistas y Perfiles Clave
        {"id": "Gerardo Sánchez Zumaya", "faccion": "Factor Financiero / Externo", "cargo": "Empresario / Aspirante Gubernatura", "color": "#d9534f", "size": 32, "foto": f"{base_url}gerardo_sanchez.jpg"},
        {"id": "José Antonio Lorca", "faccion": "Sector Empresarial Morena", "cargo": "Exdiputado Local / Operador", "color": "#8b0000", "size": 24, "foto": f"{base_url}antonio_lorca.jpg"},
        {"id": "Ana Dora Cabrera", "faccion": "Activismo / Prensa Independiente", "cargo": "Periodista / Activista", "color": "#5bc0de", "size": 22, "foto": f"{base_url}ana_dora.jpg"},
        {"id": "Paola Arreola Nieto", "faccion": "Estructura Metropolitana", "cargo": "Exdiputada Local", "color": "#8b0000", "size": 22, "foto": f"{base_url}paola_arreola.jpg"},
        {"id": "Montserrat Balcorta", "faccion": "Izquierda Ideológica / Base", "cargo": "Activista / Académica", "color": "#5bc0de", "size": 20, "foto": f"{base_url}montserrat_balcorta.jpg"},
        {"id": "Roxana Herrera", "faccion": "Militancia de Base", "cargo": "Liderazgo Social / Territorial", "color": "#8b0000", "size": 20, "foto": f"{base_url}roxana_herrera.jpg"},

        # Instituciones Clave (Nodos de Apoyo sin foto)
        {"id": "Banobras SLP", "faccion": "Institución", "cargo": "Banca de Desarrollo", "color": "#6c757d", "size": 18, "foto": None},
        {"id": "Congreso SLP", "faccion": "Institución", "cargo": "Poder Legislativo Estatal", "color": "#6c757d", "size": 18, "foto": None},
        {"id": "Delegación Bienestar", "faccion": "Institución", "cargo": "Programas Sociales", "color": "#6c757d", "size": 18, "foto": None}
    ]

    # 2. Definición de Aristas (Conexiones completas)
    relaciones = [
        # Familiares y Padrinazgo (Rojo: #c92a2a)
        {"origen": "Rosa Icela Rodríguez", "destino": "Rita Ozalia Rodríguez", "tipo": "Vínculo Sanguíneo / Protección Política", "color": "#c92a2a", "peso": 4},
        {"origen": "Ernestina Godoy", "destino": "Mario Godoy", "tipo": "Vínculo Familiar / Respaldo Federal", "color": "#c92a2a", "peso": 3},
        
        # Alianzas Operativas y Estructuras (Azul: #1c7ed6)
        {"origen": "Gabino Morales", "destino": "Guillermo Morales", "tipo": "Sucesión / Control Territorial Bienestar", "color": "#1c7ed6", "peso": 4},
        {"origen": "Gabino Morales", "destino": "Kevin Ángelo Aguilar", "tipo": "Operación Territorial (Huasteca)", "color": "#1c7ed6", "peso": 3},
        {"origen": "Rita Ozalia Rodríguez", "destino": "Carlos Arreola", "tipo": "Impulso Político / Proyecto 2027", "color": "#1c7ed6", "peso": 3},
        {"origen": "Rita Ozalia Rodríguez", "destino": "Leticia Vázquez", "tipo": "Respaldo Partidista / Lealtad Municipal", "color": "#1c7ed6", "peso": 2},
        {"origen": "Rita Ozalia Rodríguez", "destino": "Nancy Jeanine García", "tipo": "Impulso Dirigencia / Bloque Legislativo", "color": "#1c7ed6", "peso": 2},
        {"origen": "Rita Ozalia Rodríguez", "destino": "Roxana Herrera", "tipo": "Estructura de Movilización de Base", "color": "#1c7ed6", "peso": 2},
        {"origen": "Carlos Arreola", "destino": "Armando Navarro", "tipo": "Fórmula Electoral", "color": "#1c7ed6", "peso": 3},
        {"origen": "Carlos Arreola", "destino": "Paola Arreola Nieto", "tipo": "Coordinación Grupo Metropolitano", "color": "#1c7ed6", "peso": 2},
        {"origen": "José Antonio Lorca", "destino": "Cuauhtli Badillo", "tipo": "Coordinación Agenda Legislativa/Económica", "color": "#1c7ed6", "peso": 2},
        {"origen": "Armando Navarro", "destino": "Elí César Cervantes", "tipo": "Bloque de Infraestructura Federal", "color": "#1c7ed6", "peso": 2},
        {"origen": "Juan Ramiro Robledo", "destino": "Leonel Serrato", "tipo": "Coincidencia Histórica / Izquierda Tradicional", "color": "#1c7ed6", "peso": 2},
        
        # Conexiones Institucionales (Azul: #1c7ed6)
        {"origen": "Guillermo Morales", "destino": "Delegación Bienestar", "tipo": "Titularidad", "color": "#1c7ed6", "peso": 3},
        {"origen": "Armando Navarro", "destino": "Banobras SLP", "tipo": "Titularidad", "color": "#1c7ed6", "peso": 3},
        
        # Puntos de Tensión y Conflicto (Gris/Negro: #343a40)
        {"origen": "Gabino Morales", "destino": "Rita Ozalia Rodríguez", "tipo": "Disputa de Control Partidista", "color": "#343a40", "peso": 2},
        {"origen": "Carlos Arreola", "destino": "Gabino Morales", "tipo": "Competencia Interna por Gubernatura 2027", "color": "#343a40", "peso": 2},
        {"origen": "Leonel Serrato", "destino": "Rita Ozalia Rodríguez", "tipo": "Fricción Mediática / Crítica Interna", "color": "#343a40", "peso": 2},
        {"origen": "Mario Godoy", "destino": "Rita Ozalia Rodríguez", "tipo": "Distanciamiento por Cuestionamientos", "color": "#343a40", "peso": 1},
        {"origen": "Kevin Ángelo Aguilar", "destino": "Rita Ozalia Rodríguez", "tipo": "Disputa por Comités Municipales (Huasteca)", "color": "#343a40", "peso": 2},
        {"origen": "Juan Ramiro Robledo", "destino": "Carlos Arreola", "tipo": "Tensión Generacional (Vieja Guardia vs Jóvenes)", "color": "#343a40", "peso": 1},
        {"origen": "Cuauhtli Badillo", "destino": "Nancy Jeanine García", "tipo": "Competencia por Liderazgo de Bancada", "color": "#343a40", "peso": 1},
        {"origen": "Ana Dora Cabrera", "destino": "Leonel Serrato", "tipo": "Litigio por Violencia Política de Género", "color": "#343a40", "peso": 4},
        {"origen": "Gerardo Sánchez Zumaya", "destino": "Rita Ozalia Rodríguez", "tipo": "Tensión por Candidatura Gubernatura 2027", "color": "#343a40", "peso": 3},
        {"origen": "Gerardo Sánchez Zumaya", "destino": "Carlos Arreola", "tipo": "Disputa de Perfiles para 2027", "color": "#343a40", "peso": 2}
    ]

    return nodos, relaciones

def generar_html_red():
    """
    Construye el grafo en NetworkX, aplica formato en Pyvis y exporta el código HTML.
    """
    nodos, relaciones = obtener_datos_red()
    
    G = nx.DiGraph()

    # Agregar nodos con verificación de imagen
    for n in nodos:
        tooltip = f"<b>{n['id']}</b><br><b>Cargo:</b> {n['cargo']}<br><b>Facción:</b> {n['faccion']}"
        
        if n.get("foto"):
            G.add_node(
                n['id'], 
                label=n['id'], 
                title=tooltip, 
                shape="circularImage",
                image=n['foto'],
                size=n['size']
            )
        else:
            G.add_node(
                n['id'], 
                label=n['id'], 
                title=tooltip, 
                color=n['color'], 
                size=n['size']
            )

    # Agregar aristas
    for r in relaciones:
        G.add_edge(
            r['origen'], 
            r['destino'], 
            title=r['tipo'], 
            color=r['color'], 
            width=r['peso']
        )

    # Configuración de física y lienzo visual
    net = Network(
        height="650px", 
        width="100%", 
        bgcolor="#1e1e1e", 
        font_color="white", 
        directed=True
    )
    
    net.from_nx(G)

    net.set_options("""
    var options = {
      "nodes": {
        "borderWidth": 2,
        "borderWidthSelected": 4,
        "font": { "size": 13, "face": "arial", "color": "#ffffff" }
      },
      "edges": {
        "color": { "inherit": false },
        "smooth": { "type": "continuous", "roundness": 0.2 }
      },
      "physics": {
        "barnesHut": {
          "gravitationalConstant": -15000,
          "centralGravity": 0.3,
          "springLength": 130,
          "springConstant": 0.04
        }
      }
    }
    """)

    temp_dir = tempfile.gettempdir()
    path_html = os.path.join(temp_dir, "pizarra_morena_slp.html")
    net.save_graph(path_html)
    
    return path_html