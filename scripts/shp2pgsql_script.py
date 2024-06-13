import os, subprocess
from tqdm import tqdm
from psycopg_script import run_statements


def import_shapefile(conn):

    """
    Importa los shapefiles contenidos en el directorio a la base de datos PostgreSQL/PostGIS.

    Parameters:
        conn (psycopg2.connection): Conexión activa a la base de datos.
    """

    sql_drop_existing_shapefile_table = {'sql_drop_existing_shapefile_table': 'DROP TABLE IF EXISTS secciones;'}
    run_statements(conn, sql_drop_existing_shapefile_table)

    # Encontrar la ubicación de psql
    find_psql = subprocess.run(['which', 'psql'], capture_output = True, text = True, check = True)
    postgres_dir = find_psql.stdout.strip()
    postgres_bin_dir = os.path.dirname(postgres_dir)

    os.environ['PATH'] += f'{postgres_bin_dir}'
    os.environ['PGHOST'] = 'localhost'
    os.environ['PGPORT'] = '5432'
    os.environ['PGUSER'] = 'user'
    os.environ['PGPASSWORD'] = 'user'
    os.environ['PGDATABASE'] = 'TFM'

    script_dir = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
    base_dir = os.path.join(parent_dir, 'data', 'censo_ine', 'cartografia_censo2011_nacional')

    shapefile_list = []

    # Recorrer los archivos en el directorio
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.shp'):
                shapefile_list.append(os.path.join(root, file))

    # Procesar cada shapefile
    for shape_path in tqdm(shapefile_list, desc="Processing shapefiles", ncols= 100):
        cmds = f'shp2pgsql "{shape_path}" secciones | psql'
        result = subprocess.run(cmds, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode != 0:
            print(f"\nError processing {shape_path}:\n{result.stderr.decode()}")
        else:
            print(f"\nSuccessfully processed {shape_path}")

    print("All shapefiles processed.")
