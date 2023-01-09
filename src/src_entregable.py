import csv
import json

# Abrir el JSON file
#files samp.json y out_json.json
with open("data/prd/datos_imagenes.json", "r") as f:
    # Cargar la data del json a una variable en Python variable
    data_json1 = json.load(f)


with open(r'docker_files/Resultados_Encuesta.csv', encoding="utf-8") as file:
    reader = csv.reader(file)
    data_general={}
    for i in reader:
        foto=i[8]
        path=foto.split("/")
        path=path[-1]
        data_general[path]=i


c=0
info_completa=[]
for i in data_general:
    c+=1
    if(c>1):
        info_general=data_general[i]
        for j in data_json1:
            info_json=data_json1[j]
            path = j.split("/")
            path = path[-1]
            if (i==path):
                info_general.append(info_json)
                info_completa.append(info_general)


with open('data/prd/Data_entregable.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['Gerencia', 'Jefe',"Operacion","ID Cliente","Direccion","Ramo GDS","Tipo EDF","Marca","Foto"])  # Esta es la fila de encabezados
    for a in info_completa:
        writer.writerow(a)


