# Proyecto 4: Análisis de Rentabilidad y Eficiencia Operativa (BioMed Tech)

Este proyecto simula un escenario de negocio real para una empresa de servicios de mantenimiento biomédico. El objetivo fue construir un sistema de datos de extremo a extremo para identificar ineficiencias operativas, costos ocultos y evaluar el desempeño técnico.

## 📸 Dashboard Final

![Dashboard BioMed](dashboard_biomed.png)

## 💼 El Escenario de Negocio

"BioMed Tech" necesitaba responder preguntas críticas sobre su operación:
* ¿Qué equipos están consumiendo más presupuesto en mantenimiento correctivo?
* ¿Qué técnicos son eficientes (bajo tiempo, bajo costo) y cuáles necesitan capacitación?
* ¿Cuánto cuesta realmente atender cada ticket de servicio?

## 🛠️ Arquitectura de la Solución

El proyecto abarca el ciclo de vida completo de los datos:

1.  **Generación de Datos Sintéticos (Python & Faker):**
    * Creé scripts en Python para generar una base de datos realista simulando 2 años de operación.
    * Generé 4 entidades relacionadas: Clientes, Técnicos, Inventario de Equipos y Tickets de Servicio.
    * Implementé lógica de negocio compleja (ej. equipos antiguos fallan más, fechas de cierre posteriores a apertura).

2.  **Ingeniería de Datos (SQL & MySQL):**
    * Diseñé un esquema relacional en MySQL (`biomed_db`).
    * Desarrollé un script ETL en Python para cargar los datos masivos a la base de datos.
    * Creé **Vistas SQL** (`vista_finanzas_biomed`) para encapsular la lógica financiera (cálculo de horas trabajadas, costos de repuestos y mano de obra).

3.  **Business Intelligence (Power BI):**
    * Conecté Power BI directamente a la base de datos MySQL.
    * Diseñé un dashboard ejecutivo centrado en la rentabilidad y el cumplimiento de SLAs.
    * Implementé análisis de cuadrantes (Scatter Plot) para evaluar el desempeño técnico.

## 💻 Tecnologías Utilizadas

* **Python:** `pandas`, `faker`, `sqlalchemy`, `pymysql`
* **Base de Datos:** MySQL 8.0, MySQL Workbench
* **Visualización:** Microsoft Power BI
* **Lenguajes:** Python, SQL, DAX

## 🚀 Cómo Ejecutar este Proyecto

1.  Clonar el repositorio.
2.  Crear la base de datos en MySQL: `CREATE DATABASE biomed_db;`
3.  Configurar el archivo `.env` con tus credenciales de base de datos.
4.  Ejecutar los scripts de generación:
    ```bash
    python generador_datos.py
    python generador_operaciones.py
    ```
5.  Ejecutar el script de carga:
    ```bash
    python carga_sql.py
    ```
6.  Abrir el archivo `.pbix` (si se incluye) o conectar Power BI a la vista SQL generada.