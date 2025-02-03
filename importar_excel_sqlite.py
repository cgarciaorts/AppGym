import sqlite3
import pandas as pd
import openpyxl

# 📌 1. Cargar el archivo Excel
archivo_excel = "datos.xlsx"  # Asegúrate de que esté en la misma carpeta
df = pd.read_excel(archivo_excel, sheet_name=0)  # Leer la primera hoja del Excel

# 📌 2. Conectar a la base de datos SQLite
conn = sqlite3.connect("ejercicios.db")
cursor = conn.cursor()

# 📌 3. Crear la tabla (si no existe)
cursor.execute("""
CREATE TABLE IF NOT EXISTS ejercicios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ejercicio TEXT,
    series INTEGER,
    repeticiones TEXT,
    explicacion TEXT,
    rpe TEXT,
    carga INTEGER,
    categoria TEXT,
    subcategoria TEXT
)
""")

# 📌 4. Insertar los datos del Excel en SQLite
df.to_sql("ejercicios", conn, if_exists="replace", index=False)

# 📌 5. Cerrar la conexión
conn.close()

print("✅ Datos importados correctamente desde Excel a SQLite")