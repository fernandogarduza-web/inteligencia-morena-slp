import os
import tempfile
import networkx as nx
import pandas as pd
from pyvis.network import Network

def obtener_datos_red():
    """
    Define los nodos (personajes/instituciones) y las aristas (relaciones cruzadas).
    """
    base_url = "https://raw.githubusercontent.com/fernandogarduza-web/inteligencia-morena-slp/main/perfiles_morena/"

    # 1. Nodos: Se aumentaron drásticamente los tamaños (size) para que las fotos sean legibles.
    nodos = [
        # EL NODO CENTRAL
        {"id": "MORENA SLP", "faccion": "MARCA MATRIZ", "cargo": "Partido Político", "color": "#8b0000", "size": 110, "foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Morena_logo_%282014%29.svg/800px-Morena_logo_%282014%29.svg.png"},

        # Cúpula Federal
        {"id": "Rosa Icela Rodríguez", "faccion": "Cúpula Federal", "cargo": "Titular de SEGOB", "color": "#d9534f", "size": 85, "foto": f"{base_url}rosa_icela.jpg"},
        {"id": "Ernestina Godoy", "faccion": "Cúpula Federal", "cargo": "Consejera Jurídica Presidencia", "color": "#d9534f", "size": 75, "foto": f"{base_url}ernestina_godoy.jpg"},
        
        # Dirigencia y Cuadros Puros
        {"id": "Rita Ozalia Rodríguez", "faccion": "Ala Pura / Dirigencia", "cargo": "Presidenta CEE Morena", "color": "#8b0000", "size": 85, "foto": f"{base_url}rita_ozalia.jpg"},
        {"id": "Carlos Arreola", "faccion": "Ala Pura / Oficialismo", "cargo": "Diputado / Aspirante 2027", "color": "#8b0000", "size": 70, "foto": f"{base_url}carlos_arreola.jpg"},
        {"id": "Paloma Aguilar", "faccion": "Perfil Histórico Inactivo", "cargo": "Ex SAT / Fundadora", "color": "#8b0000", "size": 60, "foto": f"{base_url}paloma_aguilar.jpg"},
        
        # Grupo Gabino / Estructura Territorial
        {"id": "Gabino Morales", "faccion": "Líder Grupo Gabino", "cargo": "Diputado Federal", "color": "#0275d8", "size": 85, "foto": f"{base_url}gabino_morales.jpg"},
        {"id": "Guillermo Morales", "faccion": "Grupo Gabino", "cargo": "Súperdelegado Bienestar", "color": "#0275d8", "size": 70, "foto": f"{base_url}guillermo_morales.jpg"},
        {"id": "Kevin Ángelo Aguilar", "faccion": "Grupo Gabino", "cargo": "Diputado Fed. (Huasteca)", "color": "#0275d8", "size": 65, "foto": f"{base_url}kevin_angelo.jpg"},
        
        # Burocracia y Delegaciones Federales
        {"id": "Armando Navarro", "faccion": "Delegaciones Federales", "cargo": "Delegado de Banobras", "color": "#f0ad4e", "size": 65, "foto": f"{base_url}armando_navarro.jpg"},
        {"id": "Elí César Cervantes", "faccion": "Delegaciones Federales", "cargo": "Director SICT SLP", "color": "#f0ad4e", "size": 60, "foto": f"{base_url}eli_cesar.jpg"},
        {"id": "Mario Godoy", "faccion": "Delegaciones Federales", "cargo": "Representante INPI", "color": "#f0ad4e", "size": 60, "foto": f"{base_url}mario_godoy.jpg"},
        
        # Legislativo Local, Alcaldes y Autónomos
        {"id": "Cuauhtli Badillo", "faccion": "Legislativo Local", "cargo": "Diputado (Asp. Capital)", "color": "#5bc0de", "size": 65, "foto": f"{base_url}cuauhtli_badillo.jpg"},
        {"id": "Leonel Serrato", "faccion": "Perfil Independiente", "cargo": "Notario / Navismo Histórico", "color": "#5cb85c", "size": 65, "foto": f"{base_url}leonel_serrato.jpg"},
        {"id": "Juan Ramiro Robledo", "faccion": "Vieja Guardia", "cargo": "Legislador Federal Histórico", "color": "#d9534f", "size": 75, "foto": f"{base_url}juan_ramiro.jpg"},
        {"id": "Nancy Jeanine García", "faccion": "Ala Pura / Dirigencia", "cargo": "Diputada Local", "color": "#8b0000", "size": 60, "foto": f"{base_url}nancy_jeanine.jpg"},
        {"id": "Leticia Vázquez", "faccion": "Resistencia Municipal", "cargo": "Alcaldesa de Cerritos", "color": "#8b0000", "size": 65, "foto": f"{base_url}leticia_vazquez.jpg"},
        
        # Actores Financieros, Activistas y Perfiles Clave
        {"id": "Gerardo Sánchez", "faccion": "Factor Financiero", "cargo": "Aspirante Gubernatura", "color": "#d9534f", "size": 75, "foto": f"{base_url}gerardo_sanchez.jpg"},
        {"id": "José Antonio Lorca", "faccion": "Sector Empresarial", "cargo": "Operador / Exdiputado", "color": "#8b0000", "size": 65, "foto": f"{base_url}antonio_lorca.jpg"},
        {"id": "Ana Dora Cabrera", "faccion": "Conflictos: L. Serrato / G. Sánchez", "cargo": "Periodista / Activista", "color": "#5bc0de", "size": 65, "foto": f"{base_url}ana_dora.jpg"},
        {"id": "Paola Arreola Nieto", "faccion": "Estructura Metropolitana", "cargo": "Operadora / Exdiputada", "color": "#8b0000", "size": 60, "foto": f"{base_url}paola_arreola.jpg"},
        {"id": "Montserrat Balcorta", "faccion": "Izquierda Ideológica", "cargo": "Académica / DH", "color": "#5bc0de", "size": 60, "foto": f"{base_url}montserrat_balcorta.jpg"},
        {"id": "Roxana Herrera", "faccion": "Militancia de Base", "cargo": "Liderazgo Territorial", "color": "#8b0000", "size": 60, "foto": f"{base_url}roxana_herrera.jpg"},

        # Instituciones Clave (Sin foto, mantienen un tamaño moderado)
        {"id": "Banobras SLP", "faccion": "Institución", "cargo": "Banca de Desarrollo", "color": "#95a5a6", "size": 40, "foto": None},
        {"id": "Delegación Bienestar", "faccion": "Institución", "cargo": "Programas Sociales", "color": "#95a5a6", "size": 40, "foto": None}
    ]

    # 2. Relaciones Multidimensionales
    relaciones = [
        # CONEXIONES AL NODO CENTRAL (Gravedad hacia el partido)
        {"origen": "MORENA SLP", "destino": "Rita Ozalia Rodríguez", "tipo": "Dirigencia Estatal", "color": "#8b0000", "peso": 5},
        {"origen": "MORENA SLP", "destino": "Gabino Morales", "tipo": "Liderazgo de Facción", "color": "#8b0000", "peso": 4},
        {"origen": "MORENA SLP", "destino": "Juan Ramiro Robledo", "tipo": "Representación Histórica", "color": "#8b0000", "peso": 3},
        {"origen": "MORENA SLP", "destino": "Rosa Icela Rodríguez", "tipo": "Liderazgo Moral/Federal", "color": "#8b0000", "peso": 4},
        {"origen": "MORENA SLP", "destino": "Gerardo Sánchez", "tipo": "Aspiración Externa", "color": "#8b0000", "peso": 2},
        {"origen": "MORENA SLP", "destino": "Leticia Vázquez", "tipo": "Gobierno Municipal", "color": "#8b0000", "peso": 2},
        {"origen": "MORENA SLP", "destino": "Paloma Aguilar", "tipo": "Fundadora", "color": "#8b0000", "peso": 1},

        # Familiares y Padrinazgo Directo (Rojo: #c92a2a)
        {"origen": "Rosa Icela Rodríguez", "destino": "Rita Ozalia Rodríguez", "tipo": "Vínculo Sanguíneo", "color": "#c92a2a", "peso": 4},
        {"origen": "Ernestina Godoy", "destino": "Mario Godoy", "tipo": "Vínculo Familiar", "color": "#c92a2a", "peso": 3},
        
        # Redes de Operación y Estructura (Azul: #1c7ed6)
        {"origen": "Gabino Morales", "destino": "Guillermo Morales", "tipo": "Jefe de Grupo", "color": "#1c7ed6", "peso": 4},
        {"origen": "Gabino Morales", "destino": "Kevin Ángelo Aguilar", "tipo": "Operador Huasteca", "color": "#1c7ed6", "peso": 3},
        {"origen": "Guillermo Morales", "destino": "Mario Godoy", "tipo": "Coordinación de Delegados", "color": "#1c7ed6", "peso": 3}, # Novedad: Red burocrática cruzada
        {"origen": "Guillermo Morales", "destino": "Delegación Bienestar", "tipo": "Titular", "color": "#1c7ed6", "peso": 3},
        {"origen": "Rita Ozalia Rodríguez", "destino": "Carlos Arreola", "tipo": "Impulso 2027", "color": "#1c7ed6", "peso": 3},
        {"origen": "Rita Ozalia Rodríguez", "destino": "Nancy Jeanine García", "tipo": "Línea Congreso Local", "color": "#1c7ed6", "peso": 2},
        {"origen": "Rita Ozalia Rodríguez", "destino": "Roxana Herrera", "tipo": "Control de Bases", "color": "#1c7ed6", "peso": 2},
        {"origen": "Carlos Arreola", "destino": "Armando Navarro", "tipo": "Fórmula Electoral", "color": "#1c7ed6", "peso": 3},
        {"origen": "Carlos Arreola", "destino": "Paola Arreola Nieto", "tipo": "Alianza Zona Metropolitana", "color": "#1c7ed6", "peso": 2},
        {"origen": "Armando Navarro", "destino": "Elí César Cervantes", "tipo": "Bloque Infraestructura", "color": "#1c7ed6", "peso": 2},
        {"origen": "Armando Navarro", "destino": "Banobras SLP", "tipo": "Titular", "color": "#1c7ed6", "peso": 3},
        {"origen": "Juan Ramiro Robledo", "destino": "Leonel Serrato", "tipo": "Vieja Izquierda", "color": "#1c7ed6", "peso": 2},
        {"origen": "José Antonio Lorca", "destino": "Cuauhtli Badillo", "tipo": "Eje Económico/Legislativo", "color": "#1c7ed6", "peso": 2},
        
        # Tensiones, Pleitos y Rivalidades (Gris Oscuro/Negro: #343a40)
        {"origen": "Ana Dora Cabrera", "destino": "Leonel Serrato", "tipo": "Conflicto Legal (VPG)", "color": "#343a40", "peso": 4},
        {"origen": "Ana Dora Cabrera", "destino": "Gerardo Sánchez", "tipo": "Rivalidad Mediática", "color": "#343a40", "peso": 3}, # Novedad: Conflicto cruzado
        {"origen": "Gabino Morales", "destino": "Rita Ozalia Rodríguez", "tipo": "Control del Partido", "color": "#343a40", "peso": 3},
        {"origen": "Carlos Arreola", "destino": "Gabino Morales", "tipo": "Candidatura 2027", "color": "#343a40", "peso": 2},
        {"origen": "Leonel Serrato", "destino": "Rita Ozalia Rodríguez", "tipo": "Crítica a Dirigencia", "color": "#343a40", "peso": 2},
        {"origen": "Mario Godoy", "destino": "Rita Ozalia Rodríguez", "tipo": "Distanciamiento", "color": "#343a40", "peso": 1},
        {"origen": "Kevin Ángelo Aguilar", "destino": "Rita Ozalia Rodríguez", "tipo": "Comités Huasteca", "color": "#343a40", "peso": 2},
        {"origen": "Juan Ramiro Robledo", "destino": "Carlos Arreola", "tipo": "Choque Generacional", "color": "#343a40", "peso": 1},
        {"origen": "Gerardo Sánchez", "destino": "Rita Ozalia Rodríguez", "tipo": "Rechazo del Ala Pura", "color": "#343a40", "peso": 3},
        {"origen": "Gerardo Sánchez", "destino": "Carlos Arreola", "tipo": "Competencia 2027", "color": "#343a40", "peso": 3}
    ]

    return nodos, relaciones


def generar_html_red():
    nodos, relaciones = obtener_datos_red()
    G = nx.DiGraph()

    for n in nodos:
        # Se genera un texto multi-línea para mostrar TODA la info directamente bajo la foto
        etiqueta_visible = f"{n['id']}\n{n['cargo']}\n[{n['faccion']}]"
        
        # El tooltip emergente (al pasar el mouse)
        tooltip = f"<b>{n['id']}</b><br><b>Cargo:</b> {n['cargo']}<br><b>Facción/Perfil:</b> {n['faccion']}"
        
        if n.get("foto"):
            G.add_node(
                n['id'], 
                label=etiqueta_visible, # Se muestra abajo de la foto 
                title=tooltip, 
                shape="circularImage",
                image=n['foto'],
                size=n['size']
            )
        else:
            G.add_node(
                n['id'], 
                label=etiqueta_visible, 
                title=tooltip, 
                color=n['color'], 
                size=n['size']
            )

    for r in relaciones:
        G.add_edge(
            r['origen'], 
            r['destino'], 
            title=r['tipo'], 
            color=r['color'], 
            width=r['peso']
        )

    # El lienzo cambia a colores claros (bgcolor) y tipografía oscura (font_color)
    net = Network(
        height="750px", 
        width="100%", 
        bgcolor="#f4f6f9", 
        font_color="#2b2b2b", 
        directed=True
    )
    
    net.from_nx(G)

    # Físicas ajustadas para nodos más grandes y textos más largos
    net.set_options("""
    var options = {
      "nodes": {
        "borderWidth": 3,
        "borderWidthSelected": 6,
        "font": { 
            "size": 14, 
            "face": "system-ui, -apple-system, sans-serif", 
            "color": "#1a1a1a",
            "multi": true,
            "bold": {
                "color": "#1a1a1a",
                "size": 16
            }
        },
        "shapeProperties": {
          "useBorderWithImage": true
        }
      },
      "edges": {
        "color": { "inherit": false },
        "smooth": { "type": "continuous", "roundness": 0.15 }
      },
      "physics": {
        "barnesHut": {
          "gravitationalConstant": -35000,
          "centralGravity": 0.15,
          "springLength": 250,
          "springConstant": 0.04
        },
        "minVelocity": 0.75
      }
    }
    """)

    temp_dir = tempfile.gettempdir()
    path_html = os.path.join(temp_dir, "pizarra_morena_slp.html")
    net.save_graph(path_html)
    
    return path_html