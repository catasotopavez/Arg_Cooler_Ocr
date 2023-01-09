from keras.models import load_model
import tensorflow as tf
import os
import cv2
import numpy as np

# Carga el modelo desde el archivo
model = load_model('models/imageclassifier.h5')

barras=[]
otros=[]

dir="data/raw"
for image in os.listdir(dir):
  try:
    img = cv2.imread("data/raw/"+image)
    resize = tf.image.resize(img, (256,256))
    yhat = model.predict(np.expand_dims(resize/255, 0))
    print(yhat)
    if yhat > 0.5:
      print("No es barra")
      otros.append(image)
    else:
        print(f'Predicted class is barra')
        barras.append(image)
  except:
    print("Error")

print(f"Hay {len(barras)} imagenes de barras")
print(f"Hay {len(otros)} imagenes de otras cosas")

with open(r'docker_files/codigos_de_barra_paths.csv', 'w') as f:
  for i in barras:
    print("hola")
    if i != "image.jpg":
      f.write("data/raw/")
      f.write(i)
      f.write("\n")
