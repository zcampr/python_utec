import geopandas as gpd
import pandas as pd

# Importar excel a dataframe

registro_siniestros = pd.read_excel("data/Compilado 2022-2023_preliminar.xlsx", sheet_name="SINIESTROS", header=3)
registro_vehiculos = pd.read_excel("data/Compilado 2022-2023_preliminar.xlsx", sheet_name="VEHICULOS", header=4)
registro_personas = pd.read_excel("data/Compilado 2022-2023_preliminar.xlsx", sheet_name="PERSONAS", header=4)

# ======================================================

# LIMPIEZA DE DATOS

# Eliminar las ultimas 2 filas sin informacion para todos los registros 
registro_siniestros.drop(registro_siniestros.index[-2:], axis=0, inplace=True)
registro_vehiculos.drop(registro_vehiculos.index[-2:], axis=0, inplace=True)
registro_personas.drop(registro_personas.index[-2:], axis=0, inplace=True)

# Cambiar tipo de datos
registro_siniestros = registro_siniestros.astype({"CANTIDAD DE FALLECIDOS": "int64", "CANTIDAD DE LESIONADOS": "int64"})
registro_siniestros = registro_siniestros.iloc[:, :42]

# Convertir fecha del accidente a año / mes
def date_year(date):
    date = date[-4:]
    return date

def date_month(date):
    date = int(date[3:5])
    return date

registro_siniestros['AÑO'] = registro_siniestros['FECHA DEL ACCIDENTE'].apply(date_year)
registro_siniestros['MES'] = registro_siniestros['FECHA DEL ACCIDENTE'].apply(date_month)

# Convertir Hora del accidente a Tiempo del dia
def tiempo(hora):
    dawn = range(0, 560)
    morning = range(600, 1200)
    afternoon = range(1200, 1760)
    night = range(1800, 2400)
    hora_mod = int(hora.replace(":", ""))
    if hora_mod in dawn:
        hora = 'Madrugada'
        return hora
    if hora_mod in morning:
        hora = 'Mañana'
        return hora
    if hora_mod in afternoon:
        hora = 'Tarde'
        return hora
    if hora_mod in night:
        hora = 'Noche'
        return hora

# Convertir mes 
def num_to_month(valor_num):
    months = {1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto", 9:"Setiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"}
    for k in months:
        if valor_num == k:
            valor_num = months[k]
    return valor_num
    
registro_siniestros['TIEMPO_DEL_DIA'] = registro_siniestros['HORA DEL ACCIDENTE'].apply(tiempo)

# Quitar columnas irrelevantes para el analisis
registro_siniestros = registro_siniestros.loc[:, ['AÑO', 'MES','DEPARTAMENTO', 'PROVINCIA', 'DISTRITO', 'COORDENADAS NORTE LATITUD', 'COORDENADAS UTM ESTE LONGITUD', 'TIEMPO_DEL_DIA', 'CLASE DEL ACCIDENTE', 'SECUENCIA ACCIDENTE', 'CANTIDAD DE FALLECIDOS', 'CANTIDAD DE LESIONADOS', 'ZONA', 'CONDICIÓN CLIMÁTICA', 
'ZONIFICACIÓN', '¿EXISTE SEÑALIZACIÓN?', 'CAUSA FACTOR PRINCIPAL', 'CAUSA ESPECÍFICA']].rename(columns={'COORDENADAS NORTE LATITUD': 'COORD_LATITUD', 'COORDENADAS UTM ESTE LONGITUD': 'COORD_LONGITUD', 'CLASE DEL ACCIDENTE': 'CLASE_ACCIDENTE', 'SECUENCIA ACCIDENTE': 'SECUENCIA_ACCIDENTE','CANTIDAD DE FALLECIDOS': 'CANTIDAD_FALLECIDOS', 'CANTIDAD DE LESIONADOS': 'CANTIDAD_LESIONADOS', 'CONDICIÓN CLIMÁTICA': 'CONDICION_CLIMATICA', 'ZONIFICACIÓN': 'ZONIFICACION','¿EXISTE SEÑALIZACIÓN?': 'SEÑALIZACION','CAUSA FACTOR PRINCIPAL': 'CAUSA_PRINCIPAL','CAUSA ESPECÍFICA': 'CAUSA_ESPECIFICA'})

# Filtro Streamlit 
filter_place = registro_siniestros.loc[:, ['DEPARTAMENTO', 'PROVINCIA', 'DISTRITO']]

# Mapa de calor - Home
filter_year_month = registro_siniestros.loc[:, ['AÑO', 'MES', 'DEPARTAMENTO']]

total_year = filter_year_month.groupby(['AÑO'])[['DEPARTAMENTO']].value_counts().reset_index()

geojson = gpd.read_file('data/peru_departamental_simple.geojson')
geojson = geojson[['NOMBDEP', 'geometry']]
data_map = geojson.merge(total_year, how='left', left_on='NOMBDEP', right_on='DEPARTAMENTO')

# Cantidad de fallecidos / lesionados por: Departamento -> Provincia -> Distrito
filter_afec = registro_siniestros.loc[:, ['AÑO', 'MES', 'DEPARTAMENTO', 'PROVINCIA', 'DISTRITO', 'CANTIDAD_FALLECIDOS', 'CANTIDAD_LESIONADOS']]

# Clase de accidente por: Departamento -> Provincia -> Distrito
filter_claseacc = registro_siniestros.loc[:, ['AÑO', 'MES', 'DEPARTAMENTO', 'PROVINCIA', 'DISTRITO', 'CLASE_ACCIDENTE']]

# Tiempo del dia del accidente por: Departamento -> Provincia -> Distrito
filter_time = registro_siniestros.loc[:, ['AÑO', 'MES', 'DEPARTAMENTO', 'PROVINCIA', 'DISTRITO', 'TIEMPO_DEL_DIA']]

# Coordenadas del accidente
filter_coordinates = registro_siniestros.loc[:, ['AÑO', 'DEPARTAMENTO', 'PROVINCIA', 'DISTRITO','COORD_LATITUD', 'COORD_LONGITUD']]

# Condicion climatica durante el accidente
filter_weather = registro_siniestros.loc[:, ['AÑO', 'MES', 'DEPARTAMENTO', 'PROVINCIA', 'DISTRITO', 'CONDICION_CLIMATICA']]

# Causa principal del accidente por: Departamento -> Provincia -> Distrito
filter_principal_acc = registro_siniestros.loc[:, ['AÑO', 'MES', 'DEPARTAMENTO', 'PROVINCIA', 'DISTRITO', 'CAUSA_PRINCIPAL']]

# Causa especifica del accidente por: Departamento -> Provincia -> Distrito    
filter_especifica_acc = registro_siniestros.loc[:, ['AÑO', 'MES', 'DEPARTAMENTO', 'PROVINCIA', 'DISTRITO', 'CAUSA_ESPECIFICA']]

# Zonificacion del accidente por: Departamento -> Provincia -> Distrito    
filter_zone = registro_siniestros.loc[:, ['AÑO', 'MES', 'DEPARTAMENTO', 'PROVINCIA', 'DISTRITO', 'ZONIFICACION']]

# Data - grafico afectados en los ultimos 3 años
data_afec = filter_afec.groupby(['AÑO', 'MES'])[['CANTIDAD_FALLECIDOS', 'CANTIDAD_LESIONADOS']].sum().reset_index()
data_afec["CANTIDAD_AFECTADOS"] = data_afec['CANTIDAD_FALLECIDOS'] + data_afec['CANTIDAD_LESIONADOS']
data_afec = data_afec.drop(['CANTIDAD_FALLECIDOS', 'CANTIDAD_LESIONADOS'], axis=1)
data_afec = data_afec.groupby(by=["AÑO", "MES"])[["CANTIDAD_AFECTADOS"]].sum().reset_index()

data_afec["MES"] = data_afec["MES"].apply(num_to_month)

# Data - grafico siniestros en los ultimos 3 años
data_acc = filter_afec.groupby(["AÑO"])[["MES"]].value_counts(sort=False).reset_index()
data_acc = data_acc.rename(columns={"count": "CANTIDAD_SINIESTROS"})

data_acc["MES"] = data_acc["MES"].apply(num_to_month)

# graph_model = filter_claseacc[filter_claseacc["AÑO"] == "2023"].groupby(["AÑO", "DEPARTAMENTO"])[["CLASE_ACCIDENTE"]].value_counts().reset_index()
# print(graph_model)