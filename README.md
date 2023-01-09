# Detector de texto en imágenes

1) Primero se debe tener una carpeta con las imágenes

* Instalar los requerimientos
* Para comenzar con la detección de texto en las imágenes lo primero que se debe hacer es descargar
hacer es descargar las fotos desde gcloud a la carpeta data/raw. Esto, a través del archivo
src_download_images.py.
* Para ejecutar el código src_download_images.py. es necesario tener un archivo .csv con los resultados de la 
encuesta en la carpeta docker_files llamado "Resultados_Encuesta.csv".


* Una vez que se tienen las imágenes en la carpeta raw, se debe ejecutar el código src_main.py
el cual permite obtener los datos presentes en las imágenes.