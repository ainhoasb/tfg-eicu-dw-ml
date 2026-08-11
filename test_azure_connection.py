import pyodbc
import pandas as pd
import yaml

# 1. Cargar las credenciales desde el archivo YAML
try:
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
        
    db_config = config['azure_sql']
except FileNotFoundError:
    print("Error: No se ha encontrado el archivo config.yaml. Asegúrate de crearlo.")
    exit()

# Construcción de la cadena de conexión usando el diccionario cargado
connection_string = (
    f"DRIVER={db_config['driver']};"
    f"SERVER={db_config['server']};"
    f"PORT=1433;"
    f"DATABASE={db_config['database']};"
    f"UID={db_config['username']};"
    f"PWD={db_config['password']}"
)

try:
    # 2. Establecer la conexión
    print("Conectando a Azure...")
    conn = pyodbc.connect(connection_string)
    print("¡Conexión exitosa!")

    # 3. Consulta de prueba
    query = "SELECT TOP 10 * FROM AdmittedToICU"

    # 4. Ejecutar la consulta y volcar a Pandas
    df = pd.read_sql(query, conn)

    # 5. Mostrar los primeros resultados
    print("\nDatos extraídos correctamente:")
    print(df.head())

except Exception as e:
    print("Error durante la conexión o ejecución:", e)
    
finally:
    # Cerrar la conexión
    if 'conn' in locals():
        conn.close()
        print("\nConexión cerrada.")