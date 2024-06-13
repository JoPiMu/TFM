import psycopg2
import overpy
from tqdm import tqdm


def connect_db(options: dict):

    """
    Establece una conexión con la BBDD creada, utilizando los parámetros proporcionados en main.py.

    Parameters:
        options (dict): Un diccionario que contiene los detalles de conexión: 'dbname', 'user', 'host' y 'password'.

    Returns:
        psycopg2.connection: Una conexión activa a la base de datos.
    """

    # Conectarse a la BBDD
    try:
        conn = psycopg2.connect(
            f"dbname={options['dbname']} user={options['user']} host={options['host']} password={options['password']}"
            )
    except:
        print("I am unable to connect to the database")
    
    return conn

def run_statements(conn, initial_statements: dict = None, after_statements: dict = None, function: callable = None, function_arg: overpy.Result = None):

    """
    Ejecuta una serie de sentencias SQL en la BBDD conectada.

    Parameters:
        conn (psycopg2.connection): La conexión activa a la base de datos.
        initial_statements (dict): Un diccionario que contiene las sentencias SQL iniciales a ejecutar.
        after_statements (dict): Un diccionario que contiene las sentencias SQL finales a ejecutar.
        function (callable): Una función que se ejecutará con el argumento especificado.
        function_arg (overpy.Result): El argumento que se pasará a la función.
    """

    with conn:

        # Ejecutar las sentencias SQL iniciales
        if initial_statements is not None:
            with conn.cursor() as curs:
                try:
                    for statement in tqdm(initial_statements.values(), desc="Executing initial SQL statements", ncols= 100):
                        curs.execute(
                            statement
                        )

                except (Exception, psycopg2.DatabaseError) as error:
                    print(error)

        # Ejecutar las funciones (si son pasadas como argumentos)
        # Crea la tabla de puntos "comercios"
        if function_arg is not None:
            with conn.cursor() as curs:
                try:
                    results = function(function_arg)
                    for result in tqdm(results, desc="Appending points to the table", ncols= 100):
                        lon = result['lon']
                        lat = result['lat']
                        key = result['key']
                        type = result['type']
                        name = result['name']
                        curs.execute("""
                            INSERT INTO comercios (key, type, name, lon, lat) VALUES (%s, %s, %s, %s, %s)
                            """,
                            (key, type, name, lon, lat))

                except (Exception, psycopg2.DatabaseError) as error:
                    print(error)

        # Ejecutar las sentencias SQL finales
        if after_statements is not None:
            with conn.cursor() as curs:
                try:
                    for statement in tqdm(after_statements.values(), desc="Executing final SQL statements", ncols= 100):
                        curs.execute(
                            statement
                        )
                except (Exception, psycopg2.DatabaseError) as error:
                    print(error)

    exit

