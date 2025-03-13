import streamlit as st
import pandas as pd
import altair as alt
from urllib.error import URLError

st.set_page_config(page_title="Summary of species", page_icon="📊")

st.markdown("# Summary of species")
st.sidebar.header("Summary of species")
st.write(
    """This page shows the number of records per Phylum and per species
    """
)


def load_species_data():
    file_path = "data/GBIF_OBIS_species_list_period_2000_2020_final.csv"
    data = pd.read_csv(file_path)
    return data

# Cargar los datos
data = load_species_data()

#-------------------------------------------------------------------------------------------------------------------------------

# Contar el número de especies por Phylum
phylum_counts = data.groupby("Phylum")["species"].nunique().reset_index()
phylum_counts.columns = ["Phylum", "Number of Species"]
phylum_counts = phylum_counts.sort_values(by="Number of Species", ascending=False)  # Ordenar alfabéticamente

# Mostrar tabla con el número de especies por Phylum
st.write("## 1. Number of Species per Phylum")
st.dataframe(phylum_counts)

# Visualización opcional: gráfico de barras del número de registros por especie
st.write("### Histogram of the number of species per phylum")

chart_P = (
    alt.Chart(phylum_counts)
    .mark_bar()
    .encode(
        x=alt.X("Phylum:N", sort="-y"),
        y="Number of Species:Q",
        color="Phylum:N",
        tooltip=["Phylum", "Number of Species"]
    )
)
st.altair_chart(chart_P, use_container_width=True)

#-------------------------------------------------------------------------------------------------------------------------------

# Crear un filtro de Phylum en un selector
phylum_list = data["Phylum"].unique()
selected_phylum = st.selectbox("Select a Phylum:", phylum_list)

# Filtrar datos por Phylum seleccionado
filtered_data = data[data["Phylum"] == selected_phylum].sort_values(by="records _GBIF_OBIS", ascending=False)

# Mostrar la tabla con las especies filtradas
st.write(f"## 2. Species in Phylum: {selected_phylum}")
st.dataframe(filtered_data)

# Visualización opcional: gráfico de barras del número de registros por especie
st.write(f"### Histogram of the species in Phylum: {selected_phylum}")
chart_PS = (
    alt.Chart(filtered_data)
    .mark_bar()
    .encode(
        x=alt.X("species:N", sort="-y", title="Species"),
        y=alt.Y("records _GBIF_OBIS:Q", title="Number of Records"),
        color="species:N",
        tooltip=["species", "records _GBIF_OBIS"]
    )
)
st.altair_chart(chart_PS, use_container_width=True)


#-------------------------------------------------------------------------------------------------------------------------------

st.markdown("## 3. Number of records per species")

def get_species_data():
    df = pd.read_csv("data/Data_Occurrence_period_2000_2020.csv")
    species_counts = df.groupby("species").size().reset_index(name="count")  # Equivalente a dplyr::summarise(count = n())
    return species_counts


try:
    df = get_species_data()

    # Selector de especies
    selected_species = st.multiselect("Choose species", df["species"].unique(), [df["species"].iloc[0]])

    if not selected_species:
        st.error("Please select at least one species.")
    else:
        # Filtrar datos por especies seleccionadas
        data = df[df["species"].isin(selected_species)]

        st.write("### Histogram of the number of occurrences per species", data.sort_values("count", ascending=False))

        # Preparar datos para la visualización
        chart = (
            alt.Chart(data)
            .mark_bar()
            .encode(
                x="species:N",
                y="count:Q",
                color="species:N",
                tooltip=["species", "count"]
            )
        )

        st.altair_chart(chart, use_container_width=True)

except Exception as e:
    st.error(f"Error loading data: {e}"
    )
