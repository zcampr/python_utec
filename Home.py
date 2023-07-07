import streamlit as st
import pandas as pd
from streamlit_extras.metric_cards import style_metric_cards
from folium.features import GeoJsonTooltip
from streamlit_folium import st_folium
from filtros import graph_map_actual, graph_map_2022, graph_map_2021
from datascraper import data_actual

# Configuracion
st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed",
    page_title="Accident Analysis",
    page_icon="icons/icon_python.ico"
)

# Titulo
st.header("""
ANALISIS DE ACCIDENTES DE TRANSITO
""")

# Menu Barra Horizontal
st.sidebar.header("Prueba `v1.8`")

# Estiloss
with open('styles_css/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Contenido
st.markdown("""A día de hoy una de las principales causas de mortalidad en todo el mundo son los accidentes de tránsito, en el último informe sobre la situación mundial de la seguridad vial hecha por la OMS (2018), los accidentes de tránsito representan la octava causa de muerte, falleciendo 1,35 millones de personas y resultando en 50 millones de lesionados por año en todo el mundo. Segun el Observatorio Nacional de Seguridad Vial, ocurrieron mas de 70 000 siniestros viales dejando a mas de 3 000 fallecidos.     
            """)

st.divider()

st.subheader('Datos a nivel nacional')
col1, col2, col3 = st.columns(3)
col1.metric("Fallecidos hasta la actualidad", "###", '%## mas que el 2022')
col2.metric("La causa mas frecuente en siniestros", "txt", "%## mas que el 2022")
col3.metric("El departamento con mas siniestros", "txt", "### accidentes mas que el 2022")
style_metric_cards(background_color="#262730", 
                   border_color="#262730", 
                   border_left_color="#FDA300",
                   border_radius_px = 10)

st.divider()

st.write('"_La solucion que proponemos es un dashboard interactivo e intuitivo de facil uso para el publico en general, con datos precisos que generen consciencia en la sociedad peruana._"')

# Dividir en dos columnas
map1, map2 = st.columns(2)

with map1:
    # Data de columna 01
    option_year = st.selectbox("AÑO", ["2021", "2022", "2023"], index=2) 
    if option_year == "2023":
        year = st_folium(graph_map_actual.obtener_mapa(), width = "100%")
    elif option_year == "2022":
        year = st_folium(graph_map_2022.obtener_mapa(), width = "100%")
    elif option_year == "2021":
        year = st_folium(graph_map_2021.obtener_mapa(), width = "100%")
with map2:
    # Data de columna 02
    st.subheader("Datos de los ultimos 10 accidentes de transito hasta la fecha")
    st.divider()
    st.dataframe(data_actual, height=400)



