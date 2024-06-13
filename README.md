## Proyecto: Visor de Comercios por Secciones Censales

Este proyecto se centra en desarrollar un visor de comercios por secciones censales utilizando tecnologías como Python, JavaScript y PostgreSQL/PostGIS. A continuación, se detallan los diferentes aspectos del proyecto, incluyendo una descripción de los scripts, archivos y funcionalidades principales.

### Descripción de los Scripts de Python

1. **overpy_script.py**: Este script utiliza la biblioteca Overpy para realizar consultas a OpenStreetMap y obtener información sobre comercios en una ubicación específica. Utiliza una consulta de Overpass API para recuperar nodos de comercios, como restaurantes, bares y supermercados.

2. **new_csv_table_script.py**: Contiene funciones para crear un archivo CSV a partir de un DataFrame de Pandas. Utiliza datos del Instituto Nacional de Estadística de España (INE) para filtrar y seleccionar información relevante sobre municipios y comercios.

3. **psycopg_script.py**: Proporciona funciones para conectarse a una base de datos PostgreSQL y ejecutar sentencias SQL utilizando la biblioteca psycopg2. Se utiliza para interactuar con la base de datos y realizar operaciones como la creación de tablas y la inserción de datos.

4. **shp2pgsql_script.py**: Importa shapefiles a una base de datos PostgreSQL utilizando la herramienta shp2pgsql y psycopg2. Este script convierte archivos shapefile en comandos SQL que pueden ser ejecutados en una base de datos PostgreSQL.

5. **sql_script.py**: Contiene las sentencias SQL necesarias para crear y manipular tablas en la base de datos PostgreSQL. Estas sentencias se utilizan en conjunto con psycopg_script.py para configurar la estructura de la base de datos y realizar consultas.

6. **main.py**: El script principal que coordina la ejecución de los otros scripts para generar el visor de comercios por secciones censales. Importa y utiliza las funciones definidas en los otros scripts para crear capas de datos y controlar la interacción con la base de datos.

### Archivos JavaScript y HTML

1. **scripts.js**: Contiene el código JavaScript necesario para renderizar y controlar el mapa utilizando Leaflet y realizar solicitudes AJAX para obtener datos geojson. También define funciones para crear marcadores personalizados y agregar capas al mapa.

2. **index.html**: Es la página HTML principal que muestra el visor de mapas y carga los scripts JavaScript y hojas de estilo necesarios. Contiene la estructura básica del visor de mapas, incluyendo el contenedor del mapa y los controles de capa.

### Capas WFS y WMS

Se han creado capas WFS (Web Feature Service) y WMS (Web Map Service) a partir de GeoServer para mostrar datos geoespaciales en el visor de mapas. Estas capas proporcionan información sobre comercios y secciones censales, respectivamente. Las capas se pueden agregar al mapa utilizando Leaflet y se utilizan para visualizar y analizar datos espaciales.

### Árbol de Directorio

```
.
├── css
│   └── styles.css
├── data
│   ├── censo_ine
│   │   ├── cartografia_censo2011_nacional
│   │   ├── codccaa.xls
│   │   ├── codprov.xls
│   │   ├── indicadores_seccen_rejilla.xls
│   │   ├── indicadores_seccion_censal_csv
│   │   └── Municipios_Censo_2011.xls
│   └── styles
│       ├── points_style.sld
│       └── polygons_style.sld
├── index.html
├── js
│   ├── L.TileLayer.BetterWMS.js
│   └── scripts.js
├── plugins
│   ├── leaflet.fullscreen-master
│   ├── Leaflet-MiniMap-master
│   └── Leaflet.MousePosition-master
├── README.md
├── requirements.txt
└── scripts
    ├── main.py
    ├── new_csv_table_script.py
    ├── overpy_script.py
    ├── psycopg_script.py
    ├── shp2pgsql_script.py
    └── sql_script.py
```

Este árbol de directorio muestra la estructura de archivos y carpetas del proyecto. Contiene archivos de código fuente, datos geoespaciales y bibliotecas externas utilizadas en el proyecto.
