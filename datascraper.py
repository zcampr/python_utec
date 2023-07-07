from bs4 import BeautifulSoup
import requests
import pandas as pd

# Cargar contenido de la pagina
link = "https://www.onsv.gob.pe/"
web_content = requests.get(link)

# Convertir a objeto bs4
html_content = BeautifulSoup(web_content.content)

# Lista de accidentes actualizados
accident_list = html_content.find("div", attrs={"class", "vu-list radius"})

# Lista de fecha y hora de los accidentes 
date_time = accident_list.find_all("span")

date_acc = []
time_acc = []
type_acc = []
dep_acc = []
prov_acc = []
dist_acc = []
lat_acc = []
long_acc = []
vehicles_acc = []

# Extraer fecha y hora de los accidentes
for index in range(len(date_time)):
    elem = date_time[index]
    if index % 2 == 0:
        date_acc.append(elem.get_text().strip())
    else:
        time_acc.append(elem.get_text().strip())

# Lista la descripcion de los accidentes actualizados
descriptions = accident_list.find_all("p", attrs={"class", "mt-2"})

for descrip in descriptions:
    clean_descrip = descrip.get_text().strip().split("\r\n\t\t\t\t\t\t\t")
    type_acc.append(clean_descrip[0].replace("Clase: ", ""))
    place_acc = clean_descrip[1].replace("Lugar: ", "").strip().split(" / ")
    dep_acc.append(place_acc[0])
    prov_acc.append(place_acc[1])
    dist_acc.append(place_acc[2])
    coord_acc = clean_descrip[2].split()
    lat_acc.append(coord_acc[1])
    long_acc.append(coord_acc[2])
    vehicles_acc.append(clean_descrip[3].replace('Vehículos: ', '').strip())

# Convertir a dataframe
data_actual = pd.DataFrame({"FECHA": date_acc,
                            "HORA": time_acc, 
                            "CLASE_ACC": type_acc, 
                            "DEPARTAMENTO": dep_acc,
                            "PROVINCIA": prov_acc,
                            "DISTRITO": dist_acc,
                            "LATITUD": lat_acc,
                            "LONGITUD": long_acc,
                            "VEHICULOS": vehicles_acc})


