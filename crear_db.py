import sqlite3
import pandas as pd

# Conectar a la base de datos
conn = sqlite3.connect("ejercicios.db")
cursor = conn.cursor()

# Asegurar que la tabla ejercicios existe con la columna bloque_id
cursor.execute("""
CREATE TABLE IF NOT EXISTS ejercicios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bloque_id INTEGER,
    ejercicio TEXT,
    series INTEGER,
    repeticiones TEXT,
    explicacion TEXT,
    rpe TEXT,
    carga INTEGER,
    categoria TEXT,
    subcategoria TEXT,
    FOREIGN KEY (bloque_id) REFERENCES bloques(id)
)
""")
conn.commit()

# Función para cargar datos desde el archivo Excel sin perder bloque_id
def cargar_excel_a_db(nombre_archivo):
    df = pd.read_excel(nombre_archivo)

    # Verificar que el archivo tiene las columnas requeridas
    columnas_requeridas = {"ejercicio", "series", "repeticiones", "explicacion", "rpe", "carga", "categoria", "subcategoria"}
    if not columnas_requeridas.issubset(df.columns):
        print("❌ Error: El archivo Excel no tiene las columnas requeridas.")
        return

    # Añadir la columna bloque_id con valor NULL por defecto (si no existe en el Excel)
    if "bloque_id" not in df.columns:
        df["bloque_id"] = None  # Se podrá asignar después en la app

    # Insertar datos sin reemplazar la tabla
    df.to_sql("ejercicios", conn, if_exists="append", index=False)
    print("✅ Datos cargados correctamente desde el Excel.")

# **Ejecutar la función con el nombre de tu archivo**
nombre_archivo = "datos.xlsx"  # 📂 Cambia esto por el nombre de tu archivo Excel
cargar_excel_a_db(nombre_archivo)

# Cerrar conexión
conn.close()
