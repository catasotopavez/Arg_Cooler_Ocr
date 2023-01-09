import keras_ocr
import cv2
import csv
import re
import logging
import json
import ray
import os

ray.init()

#El siguiente código permite obtener los datos presentes en las imagenes
def get_data_path(reader):
    data = []
    for i in reader:
        data.append(i[0])
    return data
@ray.remote
def get_data(prediction_groups):
  data=[]
  for prediction in prediction_groups:
    no_texto=True
    lista_palabras=[]
    codes_in_image=[]
    for text, box in prediction:
          lista_palabras.append(text)
          code_in_text=re.findall('[0-9]+',text)
          if len(code_in_text)!=0:
            codes_in_image.append(code_in_text)
          no_texto=False

    if no_texto!=True:
      if len(codes_in_image)!=0:
        data.append(codes_in_image)


  return data

def clean_data(data):
    cleaned_data=[]
    for i in data:
        if len(i)>len(cleaned_data):
            cleaned_data=i

    return cleaned_data

#Funcion que rota 4 veces la imagen y deja la matriz (imagen) que obtiene mas datos)
@ray.remote
def rotate_image(image):
    rotated_images=[]
    height, width = image.shape[:2]
    center = (width / 2, height / 2)
    rotate_matrix_90 = cv2.getRotationMatrix2D(center=center, angle=90, scale=1)
    rotated_image_90 = cv2.warpAffine(src=image, M=rotate_matrix_90, dsize=(width, height))
    rotate_matrix_180 = cv2.getRotationMatrix2D(center=center, angle=180, scale=1)
    rotated_image_180 = cv2.warpAffine(src=image, M=rotate_matrix_180, dsize=(width, height))
    rotate_matrix_270 = cv2.getRotationMatrix2D(center=center, angle=270, scale=1)
    rotated_image_270 = cv2.warpAffine(src=image, M=rotate_matrix_270, dsize=(width, height))
    rotated_images.append(image)
    rotated_images.append(rotated_image_90)
    rotated_images.append(rotated_image_180)
    rotated_images.append(rotated_image_270)

    return rotated_images



pipeline = keras_ocr.pipeline.Pipeline()

# Open File to get Data
with open(r'docker_files/codigos_de_barra_paths.csv', encoding="utf-8") as file:
    reader = csv.reader(file)
    data = get_data_path(reader)
print(data)
data_images={}
logging.basicConfig(filename="out.log",format="%(asctime)s - %(levelname)s - %(message)s",encoding="utf-8",level=logging.DEBUG)
logging.info("Comenzando la ejecución de programa")
imagenes_revisadas=[]
for img in data:
    try:
        if(img not in imagenes_revisadas):
            imagenes_revisadas.append(img)
            image = keras_ocr.tools.read(img) #image as a matrix
            i_remote=rotate_image.remote(image)
            i=ray.get(i_remote)
            prediction_groups = pipeline.recognize(i) #Reconocer la data de las imagenes rotadas en 4
            #Get Data
            data_remote=get_data.remote(prediction_groups)
            data=ray.get(data_remote)
            #Clean Data
            cleaned_data=clean_data(data)
            data_images[img]=cleaned_data
            with open("data/prd/datos_imagenes.json", "w") as outfile:
                json.dump(data_images, outfile)
            logging.info(f"La imagen {img} ha sido cargada")
    except:
        logging.warning(f"La imagen con path: {img} no ha sido encontrada")










