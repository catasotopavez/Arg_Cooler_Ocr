import csv
import os

def get_data(reader):
    data = []
    for i in reader:
        data.append(i)
    return data


def get_link_images(rows):
    links_imagenes = []
    counter = 0
    for col in rows:
        if counter > 0:
            link = col[8]
            links_imagenes.append(link)
        counter += 1
    return links_imagenes


# Open File to get Data
data = []
with open(r'docker_files/Resultados_Encuesta.csv', encoding="utf-8") as file:
    reader = csv.reader(file)
    data = get_data(reader)

# Get links
links_images = get_link_images(data)


#Dowload Images
ccu_link=[]
for i in links_images:
    clean_link= i.split(".com/")
    ccu_forms=clean_link[1]
    print(ccu_forms)
    link="gs://"+ccu_forms
    ccu_link.append(link)

for a in ccu_link:
    p=f"gsutil cp {a} data/raw"
    os.system(p)


