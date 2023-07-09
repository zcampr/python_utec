import folium
import branca
import pandas as pd
import plotly.express as px
from folium.plugins import HeatMap, FastMarkerCluster
from datascraper import data_actual
from data_cleaning import filter_place, filter_year_month, filter_coordinates, data_afec, data_acc, geojson

class SelectPlace:
    def __init__(self, place='DEPARTAMENTO'):
        # [DATA] : Departamentos, provincias, distritos
        # Limpiar [DATA], ordenarlas alfabeticamente, eliminar duplicados y convertirlos a lista
        # place : "DEPARTAMENTO", "PROVINCIA" o "DISTRITO"
        filter_place.sort_values(place, ascending=True, inplace=True)
        self.place = place
        self.no_dup = filter_place.drop_duplicates(subset = place)
        self.lista_dep = self.no_dup[self.place].tolist()

    def get_list(self, name_place=None, all=False):
        # name_place : Provincia especifica, distrito especifico
        # all : Seleccionar "Todo"
        # Retorna solo la lista de todos los departamentos
        if self.place == 'DEPARTAMENTO' and not all:
            return self.lista_dep
        # Retorna la lista de todos los departamentos + "Todo"
        elif self.place == 'DEPARTAMENTO' and all:
            return ['Todo'] + self.lista_dep
        # Retorna solo la lista de todas las provincias
        elif self.place == 'PROVINCIA' and not all:
            self.lista_prov = self.no_dup[self.no_dup['DEPARTAMENTO'] == name_place]['PROVINCIA'].tolist()
            return self.lista_prov
        # Retorna la lista de todas las provincias + "Todo"
        elif self.place == 'PROVINCIA' and all:
            self.lista_prov = self.no_dup[self.no_dup['DEPARTAMENTO'] == name_place]['PROVINCIA'].tolist()
            return ['Todo'] + self.lista_prov
        # Retorna la lista de todos los distritos
        elif self.place == 'DISTRITO' and not all:
            self.lista_dis = self.no_dup[self.no_dup['PROVINCIA'] == name_place]['DISTRITO'].tolist()
            return self.lista_dis
        # Retorna la lista de todos los distritos + "Todo"
        elif self.place == 'DISTRITO' and all:
            self.lista_dis = self.no_dup[self.no_dup['PROVINCIA'] == name_place]['DISTRITO'].tolist()
            return ['Todo'] + self.lista_dis
        
list_dep = SelectPlace(place='DEPARTAMENTO')
list_prov = SelectPlace(place='PROVINCIA')
list_dist = SelectPlace(place='DISTRITO')

# ===========================================================
# QUITAR POR MAPA CON MARCADORES
# class SelectYear:
#     # Clase para el mapa de accidentes en los ultimos 3 años
#     # option_year : Año para mostrar info, default=2023
#     def __init__(self, option_year="2023"):
#         # Obtener cantidad de accidentes
#         self.total_year = filter_year_month.groupby(['AÑO'])[['DEPARTAMENTO']].value_counts().reset_index()
#         # Filtrar por año escogido
#         self.total_year = self.total_year.drop(self.total_year[self.total_year['AÑO'] != option_year].index)
#         self.data_final = geojson.merge(self.total_year, how="left", left_on='NOMBDEP', right_on='DEPARTAMENTO')
#         self.data_final = self.data_final.drop(['DEPARTAMENTO'], axis=1)
#         # Rellenar espacios vacios
#         self.data_final.fillna({"count": 0, 'AÑO': option_year}, inplace=True)
#         self.data_final = self.data_final[['AÑO', 'NOMBDEP', 'geometry', "count"]].rename(columns={"NOMBDEP": "DEPARTAMENTO", "geometry": 'GEOMETRY', "count": "CANTIDAD_ACCIDENTES"})

#     def obtener_mapa(self):
#         # Graficar mapa 
#         pe_map = folium.Map(location=[-9.189967, -75.015152], zoom_start=5, tiles='openstreetmap')
#         scale_map = self.data_final['CANTIDAD_ACCIDENTES'].quantile((0,0.25,0.5,0.75,1)).tolist()
#         folium.Choropleth( geo_data='data/peru_departamental_simple.geojson',
#                           data=self.data_final,
#                           columns=['DEPARTAMENTO', 'CANTIDAD_ACCIDENTES'],
#                           key_on='feature.properties.NOMBDEP',
#                           threshold_scale=scale_map,
#                           fill_color='YlOrRd',
#                           nan_fill_color="White",
#                           fill_opacity=0.7,
#                           line_opacity=0.2,
#                           highlight=True,
#                           line_color='black').add_to(pe_map)
#         return pe_map

# graph_map_actual = SelectYear(option_year="2023")
# graph_map_2022 = SelectYear(option_year="2022")
# graph_map_2021 = SelectYear(option_year="2021")
# ===========================================================
class MapMarker:
    # Clase para generar mapa de la data actualizada de la ONSV 
    def __init__(self, data=None):
        self.data_marker_map = data

    def get_map_actual(self):
        pe_map = folium.Map(location=[-9.189967, -75.015152], zoom_start=5, tiles='openstreetmap')
        def popup_html(row):
                i = row
                date = self.data_marker_map["FECHA"].iloc[i]
                hour = self.data_marker_map["HORA"].iloc[i]
                type_acc = self.data_marker_map["CLASE_ACC"].iloc[i]
                dep_name = self.data_marker_map["DEPARTAMENTO"].iloc[i]
                prov_name = self.data_marker_map["PROVINCIA"].iloc[i]
                dist_name = self.data_marker_map["DISTRITO"].iloc[i]
                lat = self.data_marker_map["LATITUD"].iloc[i]
                long = self.data_marker_map["LONGITUD"].iloc[i]
                vehicle = self.data_marker_map["VEHICULOS"].iloc[i]
                left_col_color = "#FDA300"
                right_col_color = "#f2f0d3"
                html = """<!DOCTYPE html>
            <html>
            <head>
            <h4 style="margin-bottom:10"; width="200px">DESCRIPCION DEL ACCIDENTE</h4>""" + """
            </head>
                <table style="height: 200px; width: 380px; text-align:center">
            <tbody>
            <tr>
            <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">FECHA</span></td>
            <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(date) + """
            </tr>
            <tr>
            <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">HORA</span></td>
            <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(hour) + """
            </tr>
            <tr>
            <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">CLASE DE ACCIDENTE</span></td>
            <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(type_acc) + """
            </tr>
            <tr>
            <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">DEPARTAMENTO</span></td>
            <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(dep_name) + """
            </tr>
            <tr>
            <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">PROVINCIA</span></td>
            <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(prov_name) + """
            </tr>
            <tr>
            <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">DISTRITO</span></td>
            <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(dist_name) + """
            </tr>
            <tr>
            <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">LATITUD</span></td>
            <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(lat) + """
            </tr>
            <tr>
            <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">LONGITUD</span></td>
            <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(long) + """
            </tr>
            <tr>
            <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">TIPO DE VEHICULO</span></td>
            <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(vehicle) + """
            </tr>
            </tbody>
            </table>
            </html>
            """
                return html

        for i in range(len(self.data_marker_map)):
            html = popup_html(i)
            iframe = branca.element.IFrame(html=html, width=510, height=510)
            popup = folium.Popup(folium.Html(html, script=True))
            folium.Marker([self.data_marker_map["LATITUD"].iloc[i], self.data_marker_map["LONGITUD"].iloc[i]], popup=popup, icon=folium.Icon(icon="glyphicon-info-sign",color="red")).add_to(pe_map)
        return pe_map
    
map_marker_actual = MapMarker(data=data_actual)

class PlotlyStatic:
    # Clase para generar los dos primeros graficos estaticos de la pestaña "02_Graficos"
    def __init__(self, data=None):
        # Introducir dataframe para generar el grafico
        self.data = data
    def get_graph_static(self):
        # Generar grafico de lineas
        fig_static = px.line(data_frame=self.data, 
                   x=self.data.iloc[:, 1],
                   y=self.data.iloc[:, 2],
                   color=self.data.iloc[:, 0])

        fig_static.update_layout(xaxis_title=str(self.data.columns[1]),
                       yaxis_title=str(self.data.columns[2]))
        return fig_static
    
graph_static_afec = PlotlyStatic(data=data_afec)
graph_static_acc = PlotlyStatic(data=data_acc)
        
class PlotlyGraphsAll:
    # [OPCIONES] : departamentos, provincias, distritos
    # [TIPO DE FILTRO] : Clase de accidente, condicion climatica, zonificacion, tiempo en el dia
    # Clase para generar todos los demas graficos cuando el input sea todos las [OPCIONES] segun el año
    # Se filtrara por cantidad de accidentes en todos las [OPCIONES] segun el año y el [TIPO DE FILTRO]
    # Se opto por mostrar entre las [OPCIONES] los 15 valores maximos segun el [TIPO DE FILTRO] para evitar tener demasiados valores acumulados
    # [SIN DATA] : Se uso un condicional en caso de no encontrar valores en el dataframe para graficar 
    def __init__(self, dep_all=False, prov_all=False, dis_all=False, filter_name=None, dep=None, prov=None, year=None, type_filter=None):
        # dep_all : Seleccionar "Todo" en DEPARTAMENTO
        # prov_all : Seleccionar "Todo" en PROVINCIA
        # dis_all : Seleccionar "Todo" en DISTRITO
        # filter_name : Referencia al nombre de la cada columna de [TIPO DE FILTRO] en el dataframe
        # dep : Seleccionar departamento especifico
        # prov : Seleccionar provincia especifica
        # year : Seleccionar año especifico
        # type_filter : Referencia a [TIPO DE FILTRO]
        self.data_model = pd.DataFrame()
        if dep_all:
            # Input para la opcion "Todo" en DEPARTAMENTOS, contar valores segun el [TIPO DE FILTRO]
            self.graph_model = type_filter[type_filter["AÑO"] == year].groupby(["AÑO", "DEPARTAMENTO"])[[filter_name]].value_counts().reset_index()
            # Renombrar la cantidad de accidentes
            self.graph_model = self.graph_model.rename(columns={"count": "CANTIDAD_SINIESTROS"})
            # Ordenar de mayor a menor segun la cantidad de accidentes
            self.graph_model = self.graph_model.sort_values(by=["CANTIDAD_SINIESTROS"], ascending=False)
        elif prov_all:
            # Input para la opcion "Todo" en PROVINCIAS, contar valores segun el [TIPO DE FILTRO]
            self.graph_model = type_filter[(type_filter["DEPARTAMENTO"] == dep) & (type_filter["AÑO"] == year)].groupby(["AÑO", "PROVINCIA"])[[filter_name]].value_counts().reset_index()
            # Renombrar la cantidad de accidentes
            self.graph_model = self.graph_model.rename(columns={"count": "CANTIDAD_SINIESTROS"})
            # Condicional [SIN DATA]
            if len(self.graph_model) > 0:
                self.graph_model = self.graph_model.sort_values(by=["CANTIDAD_SINIESTROS"], ascending=False)
        elif dis_all:
            # Input para la opcion "Todo" en DISTRITOS, contar valores segun el [TIPO DE FILTRO]
            self.graph_model = type_filter[(type_filter["PROVINCIA"] == prov) & (type_filter["AÑO"] == year)].groupby(["AÑO", "DISTRITO"])[[filter_name]].value_counts().reset_index()
            # Renombrar la cantidad de accidentes
            self.graph_model = self.graph_model.rename(columns={"count": "CANTIDAD_SINIESTROS"})
            # Condicional [SIN DATA]
            if len(self.graph_model) > 0:
                self.graph_model = self.graph_model.sort_values(by=["CANTIDAD_SINIESTROS"], ascending=False)
    def get_graph_all(self):
        # Generar grafico de barras segun departamento, provincia y distrito (o todos de cada uno)
        if len(self.graph_model) > 0:
            # Condicional para dataframes que no tengan accidentes reportados
            fig = px.bar(self.graph_model.iloc[:30],
                            x=self.graph_model.columns[1],
                            y=self.graph_model.columns[3],
                            color=self.graph_model.columns[2],
                            text_auto='.2s')

            # fig.update_traces(textposition='outside')
            fig.update_layout(uniformtext_minsize=8,
                                xaxis_title=None,
                                yaxis_title=None)
        # Generar un grafico vacio en caso de no tener data
        elif len(self.data_model) == 0:
            df = pd.DataFrame({"X": ["Null"],
                                "Y": ["Null"]})
            fig = px.bar(df, x="X", y="Y")
            fig.update_layout(
                                title="NO EXISTEN VALORES POR MOSTRAR")
        return fig
    def get_dataframe(self):
        return self.data_model
    
class PlotlyGraphsEspec:
    # [TIPO DE FILTRO] : Clase de accidente, condicion climatica, zonificacion, tiempo en el dia
    # Clase para filtrar y generar graficos de barras para un Distrito en especifico, clasificando segun el Mes, cantidad de siniestros y el [TIPO DE FILTRO]
    def __init__(self, type_filter=None, dis_espec=None, year_espec=None, filter_name=None):
        # type_filter : Referencia a [TIPO DE FILTRO]
        # dis_espec : Seleccionar distrito especifico
        # year_espec : Seleccionar año especifico
        # filter_name : Referencia al nombre de la cada columna de [TIPO DE FILTRO] en el dataframe
        # Limpieza de datos segun el tipo del filtro que introduzca el usuario, segun Distrito
        self.graph_espec = type_filter[(type_filter["DISTRITO"] == dis_espec) & (type_filter["AÑO"] == year_espec)].groupby(["DISTRITO", "MES"])[[filter_name]].value_counts().reset_index()
        # Renombrar columna de la cantidad de accidentes
        self.graph_espec = self.graph_espec.rename(columns={0: "CANTIDAD_ACCIDENTES"})
        # Ordenar por Mes (valor numerico)
        self.graph_espec = self.graph_espec.sort_values(by = ["MES"])
        # Eliminar duplicados
        self.lista_espec = self.graph_espec["MES"].drop_duplicates().tolist()
        # Convertir mes (int -> str)
        months = {1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto", 9:"Setiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre"}
        self.graph_espec["MES"] = self.graph_espec["MES"].replace(months)
        
    def get_graph_espec(self):
        # Generar grafico de barras segun un distrito especifico
        if len(self.graph_espec) > 0:
            fig = px.bar(self.graph_espec,
                x=self.graph_espec.columns[1],
                y=self.graph_espec.columns[3],
                color=self.graph_espec.columns[2])

            fig.update_layout(uniformtext_minsize=8,
                            xaxis_title="MES",
                            yaxis_title=None)
            return fig
        else:
            # Condicional para dataframes que no tengan accidentes reportados
            df = pd.DataFrame({"X": ["Null"],
                               "Y": ["Null"]})
            fig = px.bar(df, x="X", y="Y")
            fig.update_layout(title="NO EXISTEN VALORES POR MOSTRAR")
            return fig

class MapFolium:
    # Clase para filtrar y generar mapas de calor segun Año, Departamento, Provincia y Distrito
    def __init__(self, dep_all=False, prov_all=False, dis_all=False, dis_espec=False, dep_name=None, prov_name=None, dis_name=None, year=None):
        # dep_all : Seleccionar "Todo" en DEPARTAMENTOS, default=False
        # prov_all : Seleccionar "Todo" en PROVINCIAS, default=False
        # dis_all : Seleccionar "Todo" en DISTRITOS, default=False
        # dis_espec : Seleccionar algun distrito especifico, default=False
        # dep_name : Nombre del departamento especifico
        # prov_name : Nombre de la provincia especifica
        # dis_name : Nombre del distrito especifico
        # year : Seleccionar año especifico
        # Mapa del Peru, zoom por default = 6
        self.map_model = folium.Map(location=[-10.0000000, -76.0000000], zoom_start=6, tiles="openstreetmap")
        if dep_all:
            # Filtro por año para los datos en el mapa
            self.data_map = filter_coordinates[(filter_coordinates["AÑO"] == year)]
            self.map_model
        elif prov_all:
            # Filtro por año y departamento para los datos en el mapa
            self.data_map = filter_coordinates[(filter_coordinates["AÑO"] == year) & (filter_coordinates["DEPARTAMENTO"] == dep_name)]
            # Filtro de zoom para cada mapa
            self.zoom_coord = filter_coordinates[(filter_coordinates["AÑO"] == year) & (filter_coordinates["DEPARTAMENTO"] == dep_name)][["DEPARTAMENTO", "PROVINCIA", "COORD_LATITUD", "COORD_LONGITUD"]]
            if len(self.zoom_coord) > 0:
                # Condicional para dataframes que no tengan accidentes reportados
                self.map_model = folium.Map(location=[self.zoom_coord.iloc[0, 2], self.zoom_coord.iloc[0, 3]], zoom_start=9, tiles="openstreetmap")
            else: 
                self.map_model

        elif dis_all:
            # Filtro por año y provincia para los datos en el mapa
            self.data_map = filter_coordinates[(filter_coordinates["AÑO"] == year) & (filter_coordinates["PROVINCIA"] == prov_name)]
            # Filtro de zoom para cada mapa
            self.zoom_coord = filter_coordinates[(filter_coordinates["AÑO"] == year) & (filter_coordinates["PROVINCIA"] == prov_name)][["PROVINCIA", "DISTRITO", "COORD_LATITUD", "COORD_LONGITUD"]]
            if len(self.zoom_coord) > 0:
                # Condicional para los dataframes que no tengan accidentes reportados
                self.map_model = folium.Map(location=[self.zoom_coord.iloc[0, 2], self.zoom_coord.iloc[0, 3]], zoom_start=11, tiles="openstreetmap")
            else: 
                self.map_model

        elif dis_espec:
            # Filtro por año, provincia y distrito para los datos en el mapa
            self.data_map = filter_coordinates[(filter_coordinates["AÑO"] == year) & (filter_coordinates["PROVINCIA"] == prov_name) & (filter_coordinates["DISTRITO"] == dis_name)]
            # Filtro de zoom para cada mapa
            self.zoom_coord = filter_coordinates[(filter_coordinates["AÑO"] == year) & (filter_coordinates["PROVINCIA"] == prov_name) & (filter_coordinates["DISTRITO"] == dis_name)][["PROVINCIA", "DISTRITO", "COORD_LATITUD", "COORD_LONGITUD"]]
            if len(self.zoom_coord) > 0:
                # Condicional para los dataframes que no tengan accidentes reportados
                self.map_model = folium.Map(location=[self.zoom_coord.iloc[0, 2], self.zoom_coord.iloc[0, 3]], zoom_start=12, tiles="openstreetmap")
            else: 
                self.map_model
        # Puntos generados para la data del mapa de calor
        self.data_heat_map = self.data_map[["COORD_LATITUD", "COORD_LONGITUD"]].values
        self.data_marker_map = self.data_map[["COORD_LATITUD", "COORD_LONGITUD"]].values.tolist()

    def get_map(self):
        # Generar mapa con marcadores agrupados segun el año y el lugar
        FastMarkerCluster(self.data_marker_map,
                          control=True,
                          overlay=False).add_to(folium.FeatureGroup(name='Marcadores Agrupados').add_to(self.map_model))
        # Generar mapa de calor segun el año y el lugar
        HeatMap(self.data_heat_map,
                gradient= {0.1: 'blue', 0.3: 'lime', 0.5: 'yellow', 0.7: 'orange', 1: 'red'},
                min_opacity=0.5,
                max_zoom=18,
                name="Mapa de calor",
                radius=14,
                blur=15,
                overlay=True,
                control=True,
                show=False).add_to(self.map_model)
        folium.LayerControl().add_to(self.map_model)
        return self.map_model
    


