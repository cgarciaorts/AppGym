import sqlite3

conn = sqlite3.connect("ejercicios.db")
cursor = conn.cursor()

# Borrar la tabla ejercicios si existe
cursor.execute("DROP TABLE IF EXISTS ejercicios")

# Crear la tabla con bloque_id correctamente
cursor.execute("""
CREATE TABLE ejercicios (
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
conn.close()

print("✅ Tabla ejercicios actualizada con éxito.")
