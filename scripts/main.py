import sys
import os
import pandas as pd
import simpledbf

# Importar funciones de los scripts
from psycopg_script import connect_db, run_statements
from overpy_script import get_place_nodes, create_points_from_nodes
from new_csv_table_script import create_csv_from_df
from sql_script import sql_statements, sql_dictionaries
from shp2pgsql_script import import_shapefile

# Opciones para la BBDD
DB_OPTIONS = {
    'dbname':'TFM',
    'user':'user',
    'host':'localhost',
    'password':'user'
    }
conn = connect_db(DB_OPTIONS)

def main(place = "Lleida"):

    """Función principal del programa."""

    try:

        # Directorios del programa
        script_dir = os.path.dirname(os.path.realpath(__file__))
        parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))

        # Leer el archivo DBF i convertirlo a DF
        dbf_path = os.path.join(parent_dir, 'data', 'censo_ine', 'cartografia_censo2011_nacional', 'SECC_CPV_E_20111101_01_R_INE.dbf').replace(os.sep, '/')
        dbf = simpledbf.Dbf5(dbf_path, codec='latin1')
        df_dbf = dbf.to_dataframe()

        # Crear CSV a partir del DF con el municipio filtrado
        create_csv_from_df(place, df_dbf, parent_dir)
        
        # Obtener nodos del municipio
        comercios = get_place_nodes(place)

        # Obtener diccionarios con las sentencias SQL a ejecutar
        first_dict, second_dict = sql_dictionaries(sql_statements(place, parent_dir))

        # Ejecutar las sentencias SQL
        run_statements(conn, first_dict, second_dict, create_points_from_nodes, comercios)
        
        print("\033[1;34m🎉 End of the program. All process has been completed successfully! 🎉\033[0m")

    except Exception as e:
        print(f"\033[91mAn error has occurred: {e}\033[0m")


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("\033[91mToo few arguments!\033[0m")
    elif len(sys.argv) == 2:
        if sys.argv[1] in ["--shapefile", "-SHP"]:
            import_shapefile(conn)
        elif sys.argv[1] in ["--where", "-W"]:
            main()
        else:
            print("\033[91mIncorrect argument!\033[0m")
    elif len(sys.argv) == 3:
        if sys.argv[1] in ["--where", "-W"]:
            main(sys.argv[2])
        else:
            print("\033[91mIncorrect argument!\033[0m")
    else:
        print("\033[91mToo many arguments!\033[0m")

