import os
import csv
from tqdm import tqdm

def create_csv_from_df(place_name: str, df, global_path:str):

    """
    Crea un archivo CSV a partir de un Dataframe (Pandas) creado a partir del
    del archivo DBF del Shapefile filtrado por el municipio seleccionado, y que 
    servirá para crear la tabla que contendrá los polígonos, la población y el 
    resto de atributos (ver consultas SQL).

    Parameters:
        place_name (str): Nombre del lugar especificado en main.py.
        df (DataFrame): DataFrame de Pandas que contiene los datos.
        global_path (str): Ruta global donde se guardarán los archivos.
    """

    data_dir = os.path.join(global_path, 'data')
    for f in os.listdir(data_dir):
        if f.endswith(".csv"):
            csv_file = os.path.join(data_dir, f)
            os.remove(csv_file)

    try:
        if place_name in df['NMUN'].values:
            filtered_df = df[df['NMUN'] == place_name]
            cca_value = filtered_df['CCA'].values[0]
            pro_value = filtered_df['CPRO'].values[0]
            mun_value = filtered_df['CMUN'].values[0]
            cca_name = filtered_df['NCA'].values[0]
            pro_name = filtered_df['NPRO'].values[0]
            mun_name = filtered_df['NMUN'].values[0]
            print(f"Selected MUN: '{mun_value, mun_name}', from PRO {pro_value, pro_name}, and CA {cca_value, cca_name}")
            input_file = os.path.join(global_path, 'data', 'censo_ine', 'indicadores_seccion_censal_csv', 'C2011_ccaa{}_Indicadores.csv'.format(cca_value)).replace(os.sep, '/')
            output_file = os.path.join(global_path, 'data', 'indicadores_{}.csv'.format(place_name).replace(' ', '_'))
            exit
        else:
            print(f"\033[91mInvalid input.\033[0m")

        columns = ['ccaa', 'cpro', 'cmun', 'dist', 'secc', 't1_1']

        with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
            total_rows = sum(1 for row in infile) - 1 # Treure 1 per no comptar la capçalera

        # Abrir el archivo de entrada para lectura y el archivo de salida para escritura
        with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
            with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
            
                reader = csv.DictReader(infile)
                
                writer = csv.DictWriter(outfile, fieldnames=columns)
                
                writer.writeheader()
                
                for row in tqdm(reader, desc = "Creating CSV file", total=total_rows, ncols= 100):
                    if row['cmun'] == mun_value and row['cpro'] == pro_value and row['ccaa'] == cca_value:
                        new_row = {column: row[column] for column in columns}
                        writer.writerow(new_row)
                        
        print(f'Successfully created {output_file} with the specified columns.')

    except Exception as e:
        print(f"\033[91mAn error occurred: {e}. \nTry another input.\033[0m")
