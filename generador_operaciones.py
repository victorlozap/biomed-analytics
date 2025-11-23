import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker('es_CO')
Faker.seed(42)
random.seed(42)

# --- CARGAR DATOS MAESTROS ---
# Necesitamos los IDs que acabamos de crear para relacionarlos
try:
    df_tecnicos = pd.read_csv('dim_tecnicos.csv')
    df_clientes = pd.read_csv('dim_clientes.csv')
    ids_tecnicos = df_tecnicos['id_tecnico'].tolist()
    ids_clientes = df_clientes['id_cliente'].tolist()
except FileNotFoundError:
    print("❌ Error: No se encuentran dim_tecnicos.csv o dim_clientes.csv. Ejecuta el primer script antes.")
    exit()

# --- CONFIGURACIÓN ---
NUM_EQUIPOS = 250
FECHA_INICIO = datetime(2023, 1, 1)
FECHA_FIN = datetime(2024, 12, 31)

# Catálogo de equipos biomédicos con su complejidad (riesgo de falla y costo)
CATALOGO_EQUIPOS = [
    {'modelo': 'Rayos X Portátil RX-200', 'categoria': 'Imagenología', 'costo_base': 5000, 'prob_falla': 0.3},
    {'modelo': 'Ecógrafo Doppler E-50', 'categoria': 'Imagenología', 'costo_base': 3000, 'prob_falla': 0.2},
    {'modelo': 'Monitor Signos Vitales M-10', 'categoria': 'UCI', 'costo_base': 800, 'prob_falla': 0.1},
    {'modelo': 'Ventilador Mecánico V-Pro', 'categoria': 'UCI', 'costo_base': 12000, 'prob_falla': 0.4},
    {'modelo': 'Desfibrilador D-Heart', 'categoria': 'Emergencias', 'costo_base': 1500, 'prob_falla': 0.05}
]

def generar_equipos(n):
    """Genera el inventario instalado en los clientes."""
    data = []
    for _ in range(n):
        modelo_info = random.choice(CATALOGO_EQUIPOS)
        
        equipo = {
            'id_equipo': fake.unique.random_number(digits=6),
            'id_cliente': random.choice(ids_clientes), # Relación con cliente real
            'modelo': modelo_info['modelo'],
            'categoria': modelo_info['categoria'],
            'fecha_instalacion': fake.date_between(start_date='-5y', end_date='-2y'),
            'garantia_activa': random.choice([True, False])
        }
        data.append(equipo)
    return pd.DataFrame(data)

def generar_tickets(df_equipos):
    """
    Genera tickets de servicio históricos.
    Lógica: Equipos con alta 'prob_falla' generan más tickets.
    """
    data = []
    total_dias = (FECHA_FIN - FECHA_INICIO).days
    
    # Iteramos día por día simulando la operación (2 años)
    for dia in range(total_dias):
        fecha_actual = FECHA_INICIO + timedelta(days=dia)
        
        # Número aleatorio de fallas hoy (0 a 5 tickets diarios)
        num_tickets_hoy = random.randint(0, 5)
        
        for _ in range(num_tickets_hoy):
            # Elegimos un equipo al azar para que falle
            equipo = df_equipos.sample(1).iloc[0]
            
            # Buscamos info del modelo para ver si falla "fácil"
            info_modelo = next(item for item in CATALOGO_EQUIPOS if item['modelo'] == equipo['modelo'])
            
            # Lógica de negocio: Algunos equipos fallan más
            if random.random() > info_modelo['prob_falla']:
                continue # Este equipo tuvo suerte y no falló hoy
                
            # Si falla, creamos el ticket
            fecha_cierre = fecha_actual + timedelta(hours=random.randint(4, 72)) # Tardan entre 4 y 72h en reparar
            
            costo_repuestos = 0
            if random.random() < 0.6: # 60% de las veces se usan repuestos
                costo_repuestos = random.randint(100, int(info_modelo['costo_base'] * 0.2))

            ticket = {
                'id_ticket': fake.unique.random_number(digits=8),
                'id_equipo': equipo['id_equipo'],
                'id_tecnico': random.choice(ids_tecnicos),
                'fecha_apertura': fecha_actual,
                'fecha_cierre': fecha_cierre,
                'tipo_falla': random.choice(['Software', 'Calibración', 'Pieza Rota', 'Eléctrico']),
                'costo_repuestos': costo_repuestos
            }
            data.append(ticket)
            
    return pd.DataFrame(data)

if __name__ == "__main__":
    print("Generando datos operativos...")
    
    # 1. Generar Equipos
    df_equipos = generar_equipos(NUM_EQUIPOS)
    print(f"✅ Equipos generados: {len(df_equipos)}")
    df_equipos.to_csv('dim_equipos.csv', index=False)
    
    # 2. Generar Tickets (Basado en los equipos)
    print("⏳ Simulando 2 años de operación (esto puede tardar un poco)...")
    df_tickets = generar_tickets(df_equipos)
    print(f"✅ Tickets generados: {len(df_tickets)}")
    df_tickets.to_csv('fact_tickets.csv', index=False)