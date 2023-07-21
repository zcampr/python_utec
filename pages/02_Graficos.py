import streamlit as st
from data_cleaning import filter_claseacc, filter_weather, filter_time, filter_zone
from filtros import PlotlyGraphsAll, PlotlyGraphsEspec, list_dep, list_dist, list_prov, graph_static_afec, graph_static_acc

# Configuracion
st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed",
    page_title="Accident Analysis",
    page_icon="icons/icon_graficos.ico"
)

# Estilos
with open('styles_css/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Contenido

# Cabecera
st.header("ANÁLISIS ESTADÍSTICO DE ACCIDENTES DE TRÁNSITO")
# Separador
st.divider()
# Cabecera
st.subheader("Solo en el 2023 se reportan ya más de 1000 afectados por accidentes de tránsito...")
# Dos graficos de lineas de los ultimos 3 años
afectados, accidentes = st.columns(2)
# Grafico de la cantidad de afectados (fallecidos y lesionados)
with afectados:
    st.tabs(["AFECTADOS EN LOS ÚLTIMOS 3 AÑOS"])
    st.plotly_chart(graph_static_afec.get_graph_static(), theme="streamlit", use_container_width=True)
# Grafico de la cantidad de siniestros
with accidentes:
    st.tabs(["SINIESTROS EN LOS ÚLTIMOS 3 AÑOS"])
    st.plotly_chart(graph_static_acc.get_graph_static(), theme="streamlit", use_container_width=True)

st.divider()


st.subheader("Actualmente uno de los departamentos con mas accidentes de transito es Lima...")

# Filtro por año, departamento, provincia, distrito segun opcion del usuario
year, dep, prov, dis = st.columns(4)
with year:
    select_year = st.selectbox("AÑO", ["2021", "2022", "2023"], index=2)
with dep:
    select_dep = st.selectbox("Departamento", list_dep.get_list(name_place=None, all=True))
    if 'Todo' not in select_dep:
        with prov: 
            select_prov = st.selectbox("Provincia", list_prov.get_list(name_place=select_dep, all=True))
            if 'Todo' not in select_prov:
                with dis:
                    select_dis = st.selectbox("Distrito", list_dist.get_list(name_place=select_prov, all=True))

# Dos graficos de barras segun el año, departamento, provincia, distrito 
# FILTROS = [AÑO, DEPARTAMENTO, PROVINCIA, DISTRITO]
accident_type, weather_condition = st.columns(2)

with accident_type:
    # Grafico de cantidad de siniestros por clase de accidente segun FILTROS
    st.tabs(["SINIESTROS POR CLASE DE ACCIDENTE"])
    if "Todo" in select_dep:
        # Devolver un grafico por todos los departamentos, segun año en FILTROS
        graph_classacc = PlotlyGraphsAll(dep_all=True, year=select_year,filter_name="CLASE_ACCIDENTE", type_filter=filter_claseacc)
        st.plotly_chart(graph_classacc.get_graph_all(), theme="streamlit", use_container_width=True)
    elif "Todo" in select_prov:
        # Devolver un grafico por todos las provincias, segun el departamento y año en FILTROS
        graph_classacc = PlotlyGraphsAll(prov_all=True, year=select_year,filter_name="CLASE_ACCIDENTE", type_filter=filter_claseacc, dep=select_dep)
        st.plotly_chart(graph_classacc.get_graph_all(), theme="streamlit", use_container_width=True)
    elif "Todo" in select_dis:
        # Devolver un grafico por todos los distritos, segun la provincia y año en FILTROS
        graph_classacc = PlotlyGraphsAll(dis_all=True, year=select_year,filter_name="CLASE_ACCIDENTE", type_filter=filter_claseacc, prov=select_prov)
        st.plotly_chart(graph_classacc.get_graph_all(), theme="streamlit", use_container_width=True)
    else:
        # Devolver un grafico por todos un distrito en especifico, segun la provincia en FILTROS (especifica la cantidad por mes)
        graph_classacc = PlotlyGraphsEspec(type_filter=filter_claseacc, filter_name="CLASE_ACCIDENTE", year_espec=select_year, dis_espec=select_dis)
        st.plotly_chart(graph_classacc.get_graph_espec(), theme="streamlit", use_container_width=True)

with weather_condition:
    # Grafico de cantidad de siniestros por condicion climatica segun FILTROS
    st.tabs(["SINIESTROS POR CONDICIÓN CLIMÁTICA"])
    if "Todo" in select_dep:
        # Devolver un grafico por todos los departamentos, segun año en FILTROS
        graph_weather = PlotlyGraphsAll(dep_all=True, year=select_year,filter_name="CONDICION_CLIMATICA", type_filter=filter_weather)
        st.plotly_chart(graph_weather.get_graph_all(), theme="streamlit",use_container_width=True)
    elif "Todo" in select_prov:
        # Devolver un grafico por todos las provincias, segun el departamento y año en FILTROS
        graph_weather = PlotlyGraphsAll(prov_all=True, year=select_year,filter_name="CONDICION_CLIMATICA", type_filter=filter_weather, dep=select_dep)
        st.plotly_chart(graph_weather.get_graph_all(), theme="streamlit", use_container_width=True)
    elif "Todo" in select_dis:
        # Devolver un grafico por todos los distritos, segun la provincia y año en FILTROS
        graph_weather = PlotlyGraphsAll(dis_all=True, year=select_year,filter_name="CONDICION_CLIMATICA", type_filter=filter_weather, prov=select_prov)
        st.plotly_chart(graph_weather.get_graph_all(), theme="streamlit", use_container_width=True)
    else:
        # Devolver un grafico por todos un distrito en especifico, segun la provincia en FILTROS (especifica la cantidad por mes)
        graph_weather = PlotlyGraphsEspec(type_filter=filter_weather, filter_name="CONDICION_CLIMATICA", year_espec=select_year, dis_espec=select_dis)
        st.plotly_chart(graph_weather.get_graph_espec(), theme="streamlit", use_container_width=True)

time_day, zone = st.columns(2)

with time_day:
    # Grafico de cantidad de siniestros por tiempo en el dia segun FILTROS
    st.tabs(["SINIESTROS POR TIEMPO EN EL DÍA"])
    if "Todo" in select_dep:
        # Devolver un grafico por todos los departamentos, segun año en FILTROS
        graph_time = PlotlyGraphsAll(dep_all=True, year=select_year,filter_name="TIEMPO_DEL_DIA", type_filter=filter_time)
        st.plotly_chart(graph_time.get_graph_all(), theme="streamlit", use_container_width=True)
    elif "Todo" in select_prov:
        # Devolver un grafico por todos las provincias, segun el departamento y año en FILTROS
        graph_time = PlotlyGraphsAll(prov_all=True, year=select_year,filter_name="TIEMPO_DEL_DIA", type_filter=filter_time, dep=select_dep)
        st.plotly_chart(graph_time.get_graph_all(), theme="streamlit", use_container_width=True)
    elif "Todo" in select_dis:
        # Devolver un grafico por todos los distritos, segun la provincia y año en FILTROS
        graph_time = PlotlyGraphsAll(dis_all=True, year=select_year,filter_name="TIEMPO_DEL_DIA", type_filter=filter_time, prov=select_prov)
        st.plotly_chart(graph_time.get_graph_all(), theme="streamlit", use_container_width=True)
    else:
        # Devolver un grafico por todos un distrito en especifico, segun la provincia en FILTROS (especifica la cantidad por mes)
        graph_time = PlotlyGraphsEspec(type_filter=filter_time, filter_name="TIEMPO_DEL_DIA", year_espec=select_year, dis_espec=select_dis)
        st.plotly_chart(graph_time.get_graph_espec(), theme="streamlit", use_container_width=True)
with zone:
    # Grafico de cantidad de siniestros por zonificacion segun FILTROS
    st.tabs(["SINIESTROS POR ZONFICACIÓN"])
    if "Todo" in select_dep:
        # Devolver un grafico por todos los departamentos, segun año en FILTROS
        graph_zone = PlotlyGraphsAll(dep_all=True, year=select_year,filter_name="ZONIFICACION", type_filter=filter_zone)
        st.plotly_chart(graph_zone.get_graph_all(), theme="streamlit",use_container_width=True)
    elif "Todo" in select_prov:
        # Devolver un grafico por todos las provincias, segun el departamento y año en FILTROS
        graph_zone = PlotlyGraphsAll(prov_all=True, year=select_year,filter_name="ZONIFICACION", type_filter=filter_zone, dep=select_dep)
        st.plotly_chart(graph_zone.get_graph_all(), theme="streamlit", use_container_width=True)
    elif "Todo" in select_dis:
        # Devolver un grafico por todos los distritos, segun la provincia y año en FILTROS
        graph_zone = PlotlyGraphsAll(dis_all=True, year=select_year,filter_name="ZONIFICACION", type_filter=filter_zone, prov=select_prov)
        st.plotly_chart(graph_zone.get_graph_all(), theme="streamlit", use_container_width=True)
    else:
        # Devolver un grafico por todos un distrito en especifico, segun la provincia en FILTROS (especifica la cantidad por mes)
        graph_zone = PlotlyGraphsEspec(type_filter=filter_zone, filter_name="ZONIFICACION", year_espec=select_year, dis_espec=select_dis)
        st.plotly_chart(graph_zone.get_graph_espec(), theme="streamlit", use_container_width=True)

