# Análisis de Cultivos en Canarias

Este proyecto tiene como objetivo analizar y visualizar datos sobre cultivos en las Islas Canarias sobre el dataset abierto proporcionado por el Gobierno de Canarias.

Para ello, se ha realizado un tratamiento y análisis previo de los datos, sacando insights de los datos obtenidos. Finalmente, se ha realizado una aplicación web para poder visualizar sobre una cartografía las diferentes parcelas de cultivos por cada municipio así como algunas estadísiticas relevantes.

Puedes acceder a la aplicación web haciendo [click aquí](https://www.gobiernodecanarias.org/agricultura/temas/mapa_cultivos/).

## Requisitos

Asegúrate de tener instalado Python 3.7 o superior. Luego, instala las dependencias necesarias con el siguiente comando:

```bash
pip install geopandas seaborn folium
```

## Estructura del Proyecto

- `data-explorer`: contiene el código de la aplicación web para explorar las parcelas de cultivo.
- `analisis-cultivos.py`: notebook con el tratamiento y análisis de los datos.
- `dat/`: contiene los archivos de datos de superficies de cultivo para cada isla.

## Datos

Los datos sobre las superficies de cultivo en Canarias se pueden obtener de la página web de agricultura del Gobierno de Canarias:  
[Mapa de Cultivos de Canarias](https://www.gobiernodecanarias.org/agricultura/temas/mapa_cultivos/)  

Guarda los archivos descargados en la carpeta `dat/` de cada isla con el nombre mostrado en el notebook. También puedes descargarlo desde este enlace: (Google Drive)[https://drive.google.com/drive/folders/1t1uxBBjod_fveoJrffSo4lfWSZMxcU4_?usp=sharing]

## Explorador de datos (web)

A parte del análisis y tratamiento del dataset, se ha realizado una aplicación web para visualizar las parcelas de cultivo sobre una cartografía. Puedes acceder desde aquí.

### Despliegue de explorador de datos

TODO
