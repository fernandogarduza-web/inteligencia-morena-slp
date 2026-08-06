import os
import tempfile
import networkx as nx
import pandas as pd
from pyvis.network import Network

def obtener_datos_red():
    """
    Define los nodos (personajes/instituciones) y las aristas (relaciones).
    """
    # 1. Definición de Nodos
    nodos = [
        # Cúpula Federal
        {"id": "Rosa Icela Rodríguez", "faccion": "Cúpula Federal", "cargo": "Titular de SEGOB", "color": "#d9534f", "size": 35},
        {"id": "Ernestina Godoy", "faccion": "Cúpula Federal", "cargo": "Consejera Jurídica Presidencia", "color": "#d9534f", "size": 30},
        
        # Dirigencia y Cuadros Puros
        {"id": "Rita Ozalia Rodríguez", "faccion": "Ala Pura / Dirigencia", "cargo": "Presidenta CEE Morena SLP", "color": "#8b0000", "size": 30},
        {"id": "Carlos Arreola", "faccion": "Ala Pura / Dirigencia", "cargo": "Diputado con licencia (Aspirante Gubernatura)", "color": "#8b0000", "size": 25},
        {"id": "Paloma Aguilar", "faccion": "Ala Pura / Dirigencia", "cargo": "Ex SAT / Perfil Histórico", "color": "#8b0000", "size": 20},
        
        # Grupo Gabino / Estructura Territorial
        {"id": "Gabino Morales", "faccion": "Grupo Gabino", "cargo": "Diputado Federal", "color": "#0275d8", "size": 30},
        {"id": "Guillermo Morales", "faccion": "Grupo Gabino", "cargo": "Delegado del Bienestar SLP", "color": "#0275d8", "size": 25},
        
        # Burocracia y Delegaciones Federales
        {"id": "Armando Navarro", "faccion": "Delegaciones Federales", "cargo": "Delegado de Banobras SLP", "color": "#f0ad4e", "size": 25},
        {"id": "Elí César Cervantes", "faccion": "Delegaciones Federales", "cargo": "Director Centro SICT SLP", "color": "#f0ad4e", "size": 20},
        {"id": "Mario Godoy", "faccion": "Delegaciones Federales", "cargo": "Representante INPI SLP", "color": "#f0ad4e", "size": 20},
        
        # Cuadros Autónomos y Aspirantes
        {"id": "Cuauhtli Badillo", "faccion": "Legislativo Local", "cargo": "Diputado Local (Aspirante Capital)", "color": "#5bc0de", "size": 22},
        {"id": "Leonel Serrato", "faccion": "Perfil Independiente", "cargo": "Notario / Ex SCT Estatal", "color": "#5cb85c", "size": 22},
        
        # Instituciones Clave (Nodos de Apoyo)
        {"id": "Banobras SLP", "faccion": "Institución", "cargo": "Banca de Desarrollo", "color": "#6c757d", "size": 18},
        {"id": "Congreso SLP", "faccion": "Institución", "cargo": "Poder Legislativo Estatal", "color": "#6c757d", "size": 18},
        {"id": "Delegación Bienestar", "faccion": "Institución", "cargo": "Programas Sociales", "color": "#6c757d", "size": 18}
                # Vieja Guardia y Legisladores
        {"id": "Juan Ramiro Robledo", "faccion": "Vieja Guardia", "cargo": "Legislador Federal Histórico", "color": "#d9534f", "size": 28},
        {"id": "Kevin Ángelo Aguilar", "faccion": "Grupo Gabino", "cargo": "Diputado Federal (Huasteca)", "color": "#0275d8", "size": 22},
        {"id": "Nancy Jeanine García", "faccion": "Ala Pura / Dirigencia", "cargo": "Diputada Local", "color": "#8b0000", "size": 20},
        
        # Alcaldes
        {"id": "Leticia Vázquez", "faccion": "Bases Municipales", "cargo": "Alcaldesa de Cerritos", "color": "#8b0000", "size": 22}
    ]

    # 2. Definición de Aristas (Conexiones)
    # Colores de hilo:
    # #2b8a3e = Financiero/Recursos (Verde)
    # #1c7ed6 = Alianza/Estructura (Azul)
    # #c92a2a = Padrinazgo/Familiar (Rojo)
    # #343a40 = Tensión/Conflicto (Gris Oscuro/Negro)
    relaciones = [
        # Hilos Familiares y de Padrinazgo Directo
        {"origen": "Rosa Icela Rodríguez", "destino": "Rita Ozalia Rodríguez", "tipo": "Vínculo Sanguíneo / Protección Política", "color": "#c92a2a", "peso": 4},
        {"origen": "Ernestina Godoy", "destino": "Mario Godoy", "tipo": "Vínculo Familiar / Respaldo Federal", "color": "#c92a2a", "peso": 3},
        
        # Hilos Operativos y Hereditarios
        {"origen": "Gabino Morales", "destino": "Guillermo Morales", "tipo": "Sucesión / Control Territorial Bienestar", "color": "#1c7ed6", "peso": 4},
        {"origen": "Guillermo Morales", "destino": "Delegación Bienestar", "tipo": "Titularidad", "color": "#1c7ed6", "peso": 3},
        {"origen": "Armando Navarro", "destino": "Banobras SLP", "tipo": "Titularidad", "color": "#1c7ed6", "peso": 3},
        {"origen": "Rita Ozalia Rodríguez", "destino": "Carlos Arreola", "tipo": "Impulso Político / Proyecto 2027", "color": "#1c7ed6", "peso": 3},
        
        # Coordinación Institucional
        {"origen": "Armando Navarro", "destino": "Elí César Cervantes", "tipo": "Bloque de Infraestructura Federal", "color": "#1c7ed6", "peso": 2},
        {"origen": "Carlos Arreola", "destino": "Armando Navarro", "tipo": "Fórmula Electoral (Propietario / Suplente)", "color": "#1c7ed6", "peso": 3},
        
        # Puntos de Tensión y Conflicto
        {"origen": "Gabino Morales", "destino": "Rita Ozalia Rodríguez", "tipo": "Disputa de Control Partidista", "color": "#343a40", "peso": 2},
        {"origen": "Carlos Arreola", "destino": "Gabino Morales", "tipo": "Competencia Interna por Gubernatura 2027", "color": "#343a40", "peso": 2},
        {"origen": "Leonel Serrato", "destino": "Rita Ozalia Rodríguez", "tipo": "Fricción Mediática / Crítica Interna", "color": "#343a40", "peso": 2},
        {"origen": "Mario Godoy", "destino": "Rita Ozalia Rodríguez", "tipo": "Distanciamiento por Cuestionamientos Locales", "color": "#343a40", "peso": 1}
        # Vínculos Tercera Ronda
        {"origen": "Juan Ramiro Robledo", "destino": "Leonel Serrato", "tipo": "Coincidencia Histórica / Izquierda Tradicional", "color": "#1c7ed6", "peso": 2},
        {"origen": "Gabino Morales", "destino": "Kevin Ángelo Aguilar", "tipo": "Operación Territorial (Huasteca)", "color": "#1c7ed6", "peso": 3},
        {"origen": "Rita Ozalia Rodríguez", "destino": "Leticia Vázquez", "tipo": "Respaldo Partidista / Lealtad Municipal", "color": "#1c7ed6", "peso": 2},
        {"origen": "Rita Ozalia Rodríguez", "destino": "Nancy Jeanine García", "tipo": "Impulso Dirigencia / Bloque Legislativo", "color": "#1c7ed6", "peso": 2},
        
        # Fricciones Tercera Ronda
        {"origen": "Kevin Ángelo Aguilar", "destino": "Rita Ozalia Rodríguez", "tipo": "Disputa por Comités Municipales (Huasteca)", "color": "#343a40", "peso": 2},
        {"origen": "Juan Ramiro Robledo", "destino": "Carlos Arreola", "tipo": "Tensión Generacional (Vieja Guardia vs Jóvenes)", "color": "#343a40", "peso": 1},
        {"origen": "Cuauhtli Badillo", "destino": "Nancy Jeanine García", "tipo": "Competencia por Liderazgo de Bancada", "color": "#343a40", "peso": 1}
    ]

    return nodos, relaciones

def generar_html_red():
    """
    Construye el grafo en NetworkX, aplica formato en Pyvis y exporta el código HTML.
    """
    nodos, relaciones = obtener_datos_red()
    
    # Crear grafo dirigido
    G = nx.DiGraph()

    # Agregar nodos con atributos
    for n in nodos:
        tooltip = f"<b>{n['id']}</b><br><b>Cargo:</b> {n['cargo']}<br><b>Facción:</b> {n['faccion']}"
        G.add_node(
            n['id'], 
            label=n['id'], 
            title=tooltip, 
            color=n['color'], 
            size=n['size']
        )

    # Agregar aristas con atributos
    for r in relaciones:
        G.add_edge(
            r['origen'], 
            r['destino'], 
            title=r['tipo'], 
            color=r['color'], 
            width=r['peso']
        )

    # Configuración de la red visual interactiva
    net = Network(
        height="650px", 
        width="100%", 
        bgcolor="#1e1e1e", 
        font_color="white", 
        directed=True
    )
    
    net.from_nx(G)

    # Opciones de física para un comportamiento fluido de "telaraña"
    net.set_options("""
    var options = {
      "nodes": {
        "font": { "size": 14, "face": "arial" }
      },
      "edges": {
        "color": { "inherit": false },
        "smooth": { "type": "continuous", "roundness": 0.2 }
      },
      "physics": {
        "barnesHut": {
          "gravitationalConstant": -12000,
          "centralGravity": 0.3,
          "springLength": 120,
          "springConstant": 0.04
        },
        "minVelocity": 0.75
      }
    }
    """)

    # Guardar en archivo HTML temporal
    temp_dir = tempfile.gettempdir()
    path_html = os.path.join(temp_dir, "pizarra_morena_slp.html")
    net.save_graph(path_html)
    
    return path_html
