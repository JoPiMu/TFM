import os
from tqdm import tqdm

def sql_statements(place_name = None, global_path = None):
    '''En esta función es importante nombrar correctamente las variables.
    Si las variables empiezan por "sql1_", generaran un diccionario que se usará para ejecutarse en primer lugar (mediante psycopg_script.py).
    El resto de variables, que deberan empezar con "sql2_", generaran un segundo diccionario que se usará en último lugar.'''

    sql1_create_postgis = '''
    CREATE EXTENSION IF NOT EXISTS postgis;
    '''

    # Primero comprobamos si existen tablas existentes y, si es el caso, las eliminamos para poder ejecutar de nuevo todo el proceso:

    sql1_drop_existing_tables = '''
    DROP VIEW IF EXISTS comercios_poblacion_view;

    DROP TABLE IF EXISTS secciones_indicadores;
    DROP TABLE IF EXISTS indicadores;
    DROP TABLE IF EXISTS comercios;
    '''

    # Creamos las tablas que usaremos en el análisis SQL:

    sql1_create_table_comercios = '''
    CREATE TABLE
    comercios (
        id SERIAL PRIMARY KEY,
        key VARCHAR(60),
        type VARCHAR(60),
        name VARCHAR(60),
        lon DECIMAL(8, 6) NOT NULL,
        lat DECIMAL(9, 6) NOT NULL,
        geom geometry (Point, 4326)
    );
    '''

    sql1_create_table_indicadores = '''
    CREATE TABLE
    indicadores (
        ccaa VARCHAR(2),
        cpro VARCHAR(2),
        cmun VARCHAR(3),
        dist VARCHAR(2),
        secc VARCHAR(3),
        t1_1 INTEGER
    );
    '''

    sql1_create_table_secciones_indicadores = '''
    CREATE TABLE
    secciones_indicadores (
        id SERIAL PRIMARY KEY,
        Codigo_Seccion_Censal VARCHAR(3),
        Codigo_Distrito VARCHAR(2),
        Codigo_Municipio VARCHAR(3),
        Codigo_Provincia VARCHAR(2),
        Codigo_Comunidad_Autonoma VARCHAR(2),
        Provincia VARCHAR(50),
        Comunidad_Autonoma VARCHAR(50),
        Municipio VARCHAR(50),
        Poblacion INTEGER,
        geom GEOMETRY
    );
    '''

    # Una vez creadas las tablas, y una vez importado el shapefile de 
    # "Secciones censales" como tabla "secciones" (mediante shp2pgsql_script.py), 
    # podemos insertar los datos en las tablas.

    # Primero añadimos los elementos a la tabla "comercios" mediante psycopg2, y creamos las geometrías de puntos:

    sql2_update_table ='''
    UPDATE comercios
    SET
    geom=ST_SetSRID (ST_MakePoint (lon, lat), 4326);
    '''

    # Después importamos los datos del csv creado anteriormente (mediante new_csv_table_script.py):

    sql2_import_data_csv = '''
    COPY indicadores (ccaa, cpro, cmun, dist, secc, t1_1)
    FROM
    '{}' DELIMITER ',' CSV HEADER;
    '''.format(os.path.join(global_path, 'data', 'indicadores_{}.csv'.format(place_name)))

    # Después actualizaremos la tabla "secciones_indicadores" para que coincida con los datos de las dos tablas anteriores:

    sql2_insert_data = '''
    INSERT INTO
    secciones_indicadores (
        Codigo_Seccion_Censal,
        Codigo_Distrito,
        Codigo_Municipio,
        Codigo_Provincia,
        Codigo_Comunidad_Autonoma,
        Provincia,
        Comunidad_Autonoma,
        Municipio,
        Poblacion,
        geom
    )
    SELECT
        s.CSEC,
        s.CDIS,
        s.CMUN,
        s.CPRO,
        s.CCA,
        s.NPRO,
        s.NCA,
        s.NMUN,
        i.t1_1,
        s.geom
    FROM
        "secciones" s
    JOIN
        "indicadores" i 
    ON
        s.CPRO=i.cpro
        AND s.CMUN=i.cmun
        AND s.CSEC=i.secc
        AND s.cdis=i.dist
    WHERE
        s.CCA=i.ccaa
        AND s.CPRO=i.cpro
        AND s.CMUN=i.cmun;
    '''

    # Y asignaremos un sistema de referencia de coordenadas a la tabla "secciones_indicadores":

    sql2_set_srid = '''
    UPDATE secciones_indicadores
    SET
    geom=ST_SetSRID (geom, 25830);

    UPDATE secciones_indicadores
    SET
    geom=St_Transform (geom, 4326);
    '''

    # Finalmente, crearemos una vista con la geometría de polígonos de las secciones censales, y realizaremos la consulta
    # para ver el número de comercios que intersectan (puntos):

    sql2_create_view = '''
    CREATE VIEW comercios_poblacion_view AS
    SELECT 
        row_number() OVER () AS id,
        si.Comunidad_Autonoma,
        si.Provincia,
        si.Municipio,
        si.Codigo_Distrito,
        si.Codigo_Seccion_Censal,
        si.Poblacion,
        COUNT(c.id) AS Num_Locales,
        ROUND(((COUNT(c.id) * 100.0) / si.Poblacion)::NUMERIC, 2) AS Locales_100hab,
        si.geom
    FROM 
        secciones_indicadores si
    LEFT JOIN 
        comercios c
    ON 
        ST_Intersects(si.geom, c.geom)
    GROUP BY 
        si.Comunidad_Autonoma,
        si.Provincia,
        si.Municipio,
        si.Codigo_Distrito,
        si.Codigo_Seccion_Censal,
        si.Poblacion,
        si.geom;

    '''


    # Con la siguiente expresión, devolveremos fuera de la función todas las anteriores 
    # declaraciones SQL mediante un diccionario a través de "locals":

    return locals()

def sql_dictionaries(sql_statements_dictionary: dict):
    # A partir del diccionario generado con "locals", asignamos las variables a diccionarios 
    # diccionarios separados que servirán para ejecutarse antes o después:

    first_dict = {}
    second_dict = {}

    for key, value in tqdm(sql_statements_dictionary.items(), desc = "Adding SQL to dictionaries", ncols= 100):
        if key.startswith("sql1"):
            first_dict[key] = value.replace('\n', '')
            # print(f'Variable name "{key}" added to a dictionary')
        elif key.startswith("sql2") and key not in first_dict:
            second_dict[key] = value.replace('\n', '')
            # print(f'Variable name "{key}" added to a dictionary')
        else:
            pass


    return first_dict, second_dict