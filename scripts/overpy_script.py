import overpy
from tqdm import tqdm

def get_place_nodes(place_name: str):

    """
    Obtiene los nodos de puntos de interés de un lugar utilizando la API de Overpass.

    Parameters:
        place_name (str): Nombre del lugar del cual obtener los puntos de interés.

    Returns:
        overpy.Result: Resultado de la consulta de Overpass que contiene los nodos encontrados.
    """
        
    api = overpy.Overpass()
    query = (f"""[out:json];
            area["name"={place_name}]["admin_level"=8]->.mi_zona;
            (
            node["amenity"~"restaurant|fast_food|bar|marketplace"](area.mi_zona);
            node["shop"~"bakery|butcher|convenience|dairy|frozen_food|greengrocer|health_food|pastry|seafood|supermarket"](area.mi_zona);
            );
            out;""")
    comercios = api.query(query)
    print("Total shops found in {}:".format(place_name), len(comercios.nodes))
    return comercios

def create_points_from_nodes(overpy_return_query):

    """
    Crea puntos de interés a partir de los nodos obtenidos de la consulta de Overpass.

    Parameters:
        overpy_return_query (overpy.Result): Resultado de la consulta de Overpass que contiene los nodos.

    Returns:
        list: Lista de diccionarios que representan los puntos de interés con sus atributos.
    """

    attributes = []

    for node in tqdm(overpy_return_query.nodes, desc="Creating query points", ncols= 100):
        # Añadir elementos a la tabla
        lon = float(node.lon)
        lat = float(node.lat)

        if 'name' in node.tags:
            name = node.tags['name']
        else:
            name = None
        
        if 'amenity' in node.tags:
            key = 'amenity'
            type = node.tags['amenity']
        else:
            key = 'shop'
            type = node.tags['shop']

        attributes.append({
            'lon': lon,
            'lat': lat,
            'key': key,
            'type': type,
            'name': name
        })
        
    return attributes