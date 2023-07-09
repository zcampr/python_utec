import streamlit as st
import plotly.express as px 
from streamlit_folium import st_folium
from filtros import map_marker_actual
from datascraper import data_actual
from data_cleaning import data_home_afec, filter_principal_afec

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
st.sidebar.header("Prueba `v1.9`")

# Estiloss
with open('styles_css/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Contenido
st.markdown("""A día de hoy una de las principales causas de mortalidad en todo el mundo son los accidentes de tránsito, en el último informe sobre la situación mundial de la seguridad vial hecha por la OMS (2018), los accidentes de tránsito representan la octava causa de muerte, falleciendo 1,35 millones de personas y resultando en 50 millones de lesionados por año en todo el mundo. Segun el Observatorio Nacional de Seguridad Vial, ocurrieron mas de 70 000 siniestros viales dejando a mas de 3 000 fallecidos.     
            """)

st.divider()
st.subheader('Datos a nivel nacional')
barhome1, barhome2 = st.columns(2)
with barhome1:
    st.tabs(["CANTIDAD DE AFECTADOS POR DEPARTAMENTO"])
    graph_home1 = px.scatter(data_frame=data_home_afec, x="DEPARTAMENTO", y="CANTIDAD_AFECTADOS", color="AÑO", size="CANTIDAD_AFECTADOS", size_max=60)
    st.plotly_chart(graph_home1, use_container_width=True)

with barhome2:
    st.tabs(["CAUSAS DE ACCIDENTE EN %"])
    graph_home = px.pie(filter_principal_afec, values="CANTIDAD_AFECTADOS", names="CAUSA_PRINCIPAL", hole=.5)
    st.plotly_chart(graph_home, use_container_width=True)

st.divider()

st.write('"_La solucion que proponemos es un dashboard interactivo e intuitivo de facil uso para el publico en general, con datos precisos que generen consciencia en la sociedad peruana._"')


st.subheader("Datos de los ultimos 10 accidentes de transito hasta la fecha")
st.divider()
# Dividir en dos columnas
map1, map2 = st.columns(2)

with map1:
    # Data de columna 01
    # option_year = st.selectbox("AÑO", ["2021", "2022", "2023"], index=2) 
    # if option_year == "2023":
    #     year = st_folium(graph_map_actual.obtener_mapa(), width = "100%")
    # elif option_year == "2022":
    #     year = st_folium(graph_map_2022.obtener_mapa(), width = "100%")
    # elif option_year == "2021":
    #     year = st_folium(graph_map_2021.obtener_mapa(), width = "100%")
    ma = st_folium(map_marker_actual.get_map_actual(), width = "100%")
with map2:
    # Data de columna 02
    st.dataframe(data_actual, height=400)



