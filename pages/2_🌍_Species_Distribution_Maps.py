import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import random

st.set_page_config(page_title="Visualisation of species distribution pattern", page_icon="🌍")

st.markdown("# Species distribution maps")
st.sidebar.header("Species distribution maps")
st.write(
    """This page shows the distribution patterns of the species, based on occurrence logos downloaded from GBIF and OBIS.
    """
)

# Cargar datos
@st.cache_data
def get_species_data():
    df = pd.read_csv("data/combine_data_drop_duplicates_year.csv")
    return df

# Cargar los datos
df = get_species_data()

# Selector de especies
species_list = sorted(df["species"].unique())
selected_species = st.multiselect("Select Species to Display", species_list, default=[species_list[0]])

# Filtrar datos por especies seleccionadas
filtered_data = df[df["species"].isin(selected_species)]

# Selector para el tipo de mapa base
map_type = st.selectbox("Choose the base map type", ["CartoDB positron", "CartoDB dark_matter"])

# Crear mapa con fondo personalizado
m = folium.Map(location=[0, 0], zoom_start=2, tiles=map_type)


# Crear un diccionario para almacenar los colores seleccionados por el usuario
species_colors = {}

# Permitir al usuario seleccionar colores personalizados para cada especie
for species in selected_species:
    species_colors[species] = st.color_picker(f"Pick a color for {species}", "#FF6347")

# Añadir puntos al mapa con colores personalizados para cada especie
for _, row in filtered_data.iterrows():
    species_color = species_colors[row["species"]]  # Obtener el color seleccionado por el usuario para la especie

    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=2,  # Tamaño del punto
        color=species_color,  # Color de los puntos
        fill=True,
        fill_color=species_color,
        fill_opacity=0.6,
        popup=f"{row['species']} ({row['year']})"
    ).add_to(m)

# Agregar una leyenda con los colores correspondientes a las especies
legend_html = """
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 150px; height: 100px; 
                background-color: white; z-index:9999; border:2px solid grey; 
                font-size:14px; padding: 10px;">
        <b>Species Legend</b><br>
"""
for species, color in species_colors.items():
    legend_html += f'<i style="background-color:{color}; width: 20px; height: 20px; display: inline-block;"></i> {species}<br>'

legend_html += "</div>"

# Agregar la leyenda al mapa
m.get_root().html.add_child(folium.Element(legend_html))

# Mostrar mapa en Streamlit
st.write("### Species Occurrence Map 🌍")
folium_static(m)



















