import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv

# --- CONFIGURACIÓN ---
load_dotenv() # Carga las credenciales del archivo .env

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

# Validar conexión
if not all([DB_HOST, DB_USER, DB_PASSWORD, DB_NAME]):
    print("❌ Error: Faltan variables en el archivo .env")
    exit()

def obtener_engine():
    """Crea la conexión a MySQL usando PyMySQL"""
    password_esc = quote_plus(DB_PASSWORD)
    cadena = f"mysql+pymysql://{DB_USER}:{password_esc}@{DB_HOST}/{DB_NAME}"
    return create_engine(cadena)

def cargar_tabla(nombre_archivo, nombre_tabla, engine):
    """Lee un CSV y lo carga a SQL"""
    try:
        print(f"📂 Leyendo {nombre_archivo}...")
        df = pd.read_csv(nombre_archivo)
        
        # Conversión de fechas (importante para SQL)
        # Buscamos columnas que tengan 'fecha' en el nombre
        for col in df.columns:
            if 'fecha' in col:
                df[col] = pd.to_datetime(df[col])
        
        print(f"➡️ Cargando {len(df)} filas en la tabla '{nombre_tabla}'...")
        
        # if_exists='replace' borrará la tabla si ya existe y la creará de nuevo
        # index=False evita que se guarde el índice numérico de Pandas (0,1,2...)
        df.to_sql(nombre_tabla, con=engine, if_exists='replace', index=False)
        
        print("✅ Carga exitosa.\n")
        
    except Exception as e:
        print(f"❌ Error cargando {nombre_tabla}: {e}")

# --- EJECUCIÓN ---
if __name__ == "__main__":
    engine = obtener_engine()
    print("--- INICIANDO CARGA A BASE DE DATOS BIOMÉDICA ---\n")
    
    # 1. Cargar Dimensiones (Las tablas "Padre")
    cargar_tabla('dim_clientes.csv', 'dim_clientes', engine)
    cargar_tabla('dim_tecnicos.csv', 'dim_tecnicos', engine)
    
    # 2. Cargar Inventario (Depende de Clientes)
    cargar_tabla('dim_equipos.csv', 'dim_equipos', engine)
    
    # 3. Cargar Hechos (Depende de Equipos y Técnicos)
    cargar_tabla('fact_tickets.csv', 'fact_tickets', engine)
    
    print("--- PROCESO FINALIZADO ---")