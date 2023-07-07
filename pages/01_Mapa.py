import folium
import streamlit as st
from filtros import list_dep, list_dist, list_prov
from streamlit_folium import st_folium
from streamlit_extras.badges import badge
from filtros import MapFolium

# Configuracion
st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed",
    page_title="Accident Analysis",
    page_icon="icons/icon_map.ico"
)

# Estiloss
with open('styles_css/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Barra Lateral
with st.sidebar:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("`Codigo en Github`")
    with col2:
        badge(type="github", name="zcampr/python_utec")


# Cabecera
st.header("MAPA GEOGRAFICO SOBRE SINIESTROS EN EL PAIS")

# Caja de seleccion multiple
year, dep, prov, dis = st.columns(4)
# Para año
with year:
    select_year = st.selectbox("AÑO", ["2021", "2022", "2023"], index=2)
# Para Departamento, Provincia, Distrito
with dep:
    select_dep = st.selectbox("DEPARTAMENTO", list_dep.get_list(name_place=None, all=True))
    if 'Todo' not in select_dep:
        with prov: 
            select_prov = st.selectbox("PROVINCIA", list_prov.get_list(name_place=select_dep, all=True))
            if 'Todo' not in select_prov:
                with dis:
                    select_dis = st.selectbox("DISTRITO", list_dist.get_list(name_place=select_prov, all=True))

# Mas informacion -> filtros.py
# Seleccionar mapa con info segun el input del usuario
if "Todo" in select_dep:
    geo_map = MapFolium(dep_all=True, year=select_year)
elif "Todo" in select_prov:
    geo_map = MapFolium(prov_all=True, dep_name=select_dep, year=select_year)
elif "Todo" in select_dis:
    geo_map = MapFolium(dis_all=True, prov_name=select_prov, year=select_year)
elif select_dis:
    geo_map = MapFolium(dis_espec=True, prov_name=select_prov, dis_name=select_dis, year=select_year)

# Mostrar mapa en streamlit
year = st_folium(geo_map.get_map(), width = "100%", height=850)
