import streamlit as st
from data_cleaning import filter_claseacc, filter_time, filter_afec, filter_weather, filter_principal_acc, filter_especifica_acc

# Configuracion
st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed",
    page_title="Accident Analysis",
    page_icon="icons/icon_table.ico"
)

# Estiloss
with open('styles_css/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Headers
st.header("TABLAS DE INFORMACION")

st.divider()

# Dataframes
st.subheader("Clase de siniestro por Departamento / Provincia / Distrito")
clase_tabla, clase_code = st.columns(2)
with clase_tabla:
    st.dataframe(filter_claseacc, use_container_width=True)
    @st.cache_data
    def convertir_df(df):
        return df.to_csv(index=False).encode('utf-8')
    csv1 = convertir_df(filter_claseacc)
    st.download_button(
        label="Clases_siniestros_csv",
        data=csv1,
        file_name="Clases_siniestros_2021_2023.csv",
        mime='text/csv',
    )
with clase_code:
    st.code("""
    # CODIGO - TEMPORAL

    st.dataframe(filter_claseacc, use_container_width=True)

    @st.cache_data
    def convertir_df(df):
        return df.to_csv(index=False).encode('utf-8')

    csv1 = convertir_df(filter_claseacc)

    st.download_button(
        label="Clases_siniestros_csv",
        data=csv1,
        file_name="Clases_siniestros_2021_2023.csv",
        mime='text/csv',
    )
    """, language="python")
# ==========================================================
st.subheader("Tiempo del dia del siniestro por Departamento / Provincia / Distrito")
time_table, time_code = st.columns(2)
with time_table:
    st.dataframe(filter_time, use_container_width=True)
    @st.cache_data
    def convertir_df(df):
        return df.to_csv().encode('utf-8')
    csv = convertir_df(filter_time)
    st.download_button(
        label="Tiempo_siniestros_csv",
        data=csv,
        file_name="Tiempo_siniestros_2021_2023.csv",
        mime='text/csv',
    )
with time_code:
    st.code("""
    # CODIGO - TEMPORAL
      
    st.dataframe(filter_time, use_container_width=True)

    @st.cache_data
    def convertir_df(df):
        return df.to_csv().encode('utf-8')

    csv = convertir_df(filter_time)

    st.download_button(
        label="Tiempo_siniestros_csv",
        data=csv,
        file_name="Tiempo_siniestros_2021_2023.csv",
        mime='text/csv',
    )
    """)
# ==========================================================
st.subheader("Cantidad de afectados por siniestro por Departamento / Provincia / Distrito")
afec_table, afec_code = st.columns(2)
with afec_table:
    st.dataframe(filter_afec, use_container_width=True)
    @st.cache_data
    def convertir_df(df):
        return df.to_csv().encode('utf-8')
    csv = convertir_df(filter_afec)
    st.download_button(
        label="Afectados_siniestros_csv",
        data=csv,
        file_name="Tiempo_accidente_2021_2023.csv",
        mime='text/csv',
    )
with afec_code:
    st.code("""
    # CODIGO - TEMPORAL

    st.dataframe(filter_afec, use_container_width=True)

    @st.cache_data
    def convertir_df(df):
        return df.to_csv().encode('utf-8')

    csv = convertir_df(filter_afec)

    st.download_button(
        label="Afectados_siniestros_csv",
        data=csv,
        file_name="Tiempo_accidente_2021_2023.csv",
        mime='text/csv',
    )
    """)
# ==========================================================
st.subheader("Condicion climatica del siniestro por Departamento / Provincia / Distrito")
weather_table, weather_code = st.columns(2)
with weather_table:
    st.dataframe(filter_weather, use_container_width=True)
    @st.cache_data
    def convertir_df(df):
        return df.to_csv().encode('utf-8')
    csv = convertir_df(filter_weather)
    st.download_button(
        label="Clima_siniestros_csv",
        data=csv,
        file_name="Climas_siniestros_2021_2023.csv",
        mime='text/csv',
    )
with weather_code:
    st.code("""
    # CODIGO - TEMPORAL

    st.dataframe(filter_weather, use_container_width=True)

    @st.cache_data
    def convertir_df(df):
        return df.to_csv().encode('utf-8')

    csv = convertir_df(filter_weather)

    st.download_button(
        label="Clima_siniestros_csv",
        data=csv,
        file_name="Climas_siniestros_2021_2023.csv",
        mime='text/csv',
    )
    """)
# ==========================================================
st.subheader("Causa principal del siniestro por Departamento / Provincia / Distrito")
principal_table, principal_code = st.columns(2)
with principal_table:
    st.dataframe(filter_principal_acc, use_container_width=True)
    @st.cache_data
    def convertir_df(df):
        return df.to_csv().encode('utf-8')
    csv = convertir_df(filter_principal_acc)
    st.download_button(
        label="Causa_principal_csv",
        data=csv,
        file_name="Causaprin_siniestros_2021_2023.csv",
        mime='text/csv',
    )
with principal_code:
    st.code("""
    # CODIGO - TEMPORAL

    st.dataframe(filter_principal_acc, use_container_width=True)

    @st.cache_data
    def convertir_df(df):
        return df.to_csv().encode('utf-8')

    csv = convertir_df(filter_principal_acc)

    st.download_button(
        label="Causa_principal_csv",
        data=csv,
        file_name="Causaprin_siniestros_2021_2023.csv",
        mime='text/csv',
    )
    """)
# ==========================================================
st.subheader("Causa especifica del siniestro por Departamento / Provincia / Distrito")
espec_table, espec_code = st.columns(2)
with espec_table:
    st.dataframe(filter_especifica_acc, use_container_width=True)
    @st.cache_data
    def convertir_df(df):
        return df.to_csv().encode('utf-8')
    csv = convertir_df(filter_especifica_acc)
    st.download_button(
        label="Causa_especifica_csv",
        data=csv,
        file_name="Causaespec_siniestros_2021_2023.csv",
        mime='text/csv',
    )
with espec_code:
    st.code("""
    # CODIGO - TEMPORAL

    st.dataframe(filter_especifica_acc, use_container_width=True)

    @st.cache_data
    def convertir_df(df):
        return df.to_csv().encode('utf-8')

    csv = convertir_df(filter_especifica_acc)

    st.download_button(
        label="Causa_especifica_csv",
        data=csv,
        file_name="Causaespec_siniestros_2021_2023.csv",
        mime='text/csv',
    )
    """)