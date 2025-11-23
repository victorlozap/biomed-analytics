import pandas as pd
from faker import Faker
import random

# Inicializamos Faker con configuración regional (opcional, para nombres latinos)
fake = Faker('es_CO') # Puedes cambiar 'es_CO' por 'es_ES' o 'es_MX'

# --- CONFIGURACIÓN DE VOLUMEN (Lo que acordamos) ---
NUM_CLIENTES = 40
NUM_TECNICOS = 12
NUM_EQUIPOS = 250

# Semilla para que los datos sean siempre los mismos si corres el script de nuevo
Faker.seed(42)
random.seed(42)

def generar_tecnicos(n):
    """Genera una lista de técnicos con sus costos por hora."""
    data = []
    roles = ['Junior', 'Senior', 'Especialista']
    
    for _ in range(n):
        rol = random.choice(roles)
        # El costo depende del rol
        if rol == 'Junior': costo = random.randint(20, 35)
        elif rol == 'Senior': costo = random.randint(40, 60)
        else: costo = random.randint(70, 100)
        
        tecnico = {
            'id_tecnico': fake.unique.random_number(digits=4),
            'nombre': fake.name(),
            'rol': rol,
            'costo_hora': costo,
            'ciudad_base': fake.city()
        }
        data.append(tecnico)
    return pd.DataFrame(data)

def generar_clientes(n):
    """Genera hospitales y clínicas."""
    data = []
    tipos = ['Hospital', 'Clínica', 'Centro Médico', 'Laboratorio']
    
    for _ in range(n):
        tipo = random.choice(tipos)
        nombre_inst = f"{tipo} {fake.company()}"
        
        cliente = {
            'id_cliente': fake.unique.random_number(digits=5),
            'nombre': nombre_inst,
            'ciudad': fake.city(),
            'direccion': fake.address(),
            'telefono': fake.phone_number()
        }
        data.append(cliente)
    return pd.DataFrame(data)

# --- EJECUCIÓN ---
if __name__ == "__main__":
    print("Generando datos maestros...")
    
    # 1. Generar Técnicos
    df_tecnicos = generar_tecnicos(NUM_TECNICOS)
    print(f"✅ Técnicos generados: {len(df_tecnicos)}")
    print(df_tecnicos.head())
    
    # 2. Generar Clientes
    df_clientes = generar_clientes(NUM_CLIENTES)
    print(f"\n✅ Clientes generados: {len(df_clientes)}")
    print(df_clientes.head())
    
    # Guardar en CSV para verlos (Backup)
    df_tecnicos.to_csv('dim_tecnicos.csv', index=False)
    df_clientes.to_csv('dim_clientes.csv', index=False)